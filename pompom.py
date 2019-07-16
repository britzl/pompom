#!/usr/bin/env python

import urllib
import zipfile
import os
import sys
import shutil
import fnmatch
import json
import tempfile
from xml.dom.minidom import parseString
from xml.dom import minidom
from subprocess import call
from argparse import ArgumentParser
from contextlib import contextmanager


def javac(file):
    javac = "javac -source 1.7 -target 1.7 %s" % (file)
    call(javac, shell=True)

def get_element_value(element):
    if element and element.childNodes:
        return element.childNodes[0].nodeValue
    else:
        return None

def get_child_element(xml_document, tag_name):
    if xml_document is None:
        return None
    for child in xml_document.childNodes:
        if child.nodeName == tag_name:
            return child
    return None

def get_child_value(xml_document, tag_name):
    child = get_child_element(xml_document, tag_name)
    return get_element_value(child)

def get_xml_elements(xml_document, tag_name):
    if xml_document and xml_document.getElementsByTagName(tag_name):
        return xml_document.getElementsByTagName(tag_name)
    else:
        return {}


def get_xml_element(xml_document, tag_name, index=0):
    if xml_document and xml_document.getElementsByTagName(tag_name):
        return xml_document.getElementsByTagName(tag_name)[index]
    else:
        return None

def get_xml_value(xml_document, tag_name, default=None):
    if xml_document and xml_document.getElementsByTagName(tag_name):
        node = xml_document.getElementsByTagName(tag_name)[0]
        return get_element_value(node)
    else:
        return default


def has_duplicate_xml_node(xml_document, node):
    nodes = get_xml_elements(xml_document, node.nodeName)
    for n in nodes:
        if n.toxml() == node.toxml():
            return True
    return False


def prettify_xml(xml_document):
    reparsed = parseString(xml_document.toxml())
    return '\n'.join([line for line in reparsed.toprettyxml(indent=' '*2, encoding="utf-8").split('\n') if line.strip()])


def create_empty_manifest(filename):
    with open(filename, "w") as file:
        file.write('<?xml version="1.0" encoding="utf-8"?>\n<manifest xmlns:android="http://schemas.android.com/apk/res/android"\n    package="{{android.package}}">\n    <uses-sdk android:minSdkVersion="9"/>\n    <application>\n    </application></manifest>')


def merge_manifest_files(src_manifest_name, dst_manifest_name, name):
    with open(dst_manifest_name, "r") as dst_file:
        dst_manifest = dst_file.read().replace("\" />", "\"/>")

    # get nodes to work on
    src_xmldoc = minidom.parse(src_manifest_name)
    src_manifest = get_xml_element(src_xmldoc, "manifest")
    src_application = get_xml_element(src_manifest, "application")
    package = src_manifest.getAttribute("package")
    comment = src_xmldoc.createComment(package)
    print("Merging AndroidManifest.xml from {}".format(package))

    # merge manifest level nodes
    for tag in ["uses-permission", "permission"]:
        for node in get_xml_elements(src_manifest, tag):
            node_xml = node.toxml().replace("${applicationId}", "{{android.package}}")
            if node_xml not in dst_manifest:
                dst_manifest = dst_manifest.replace("</manifest>", "\t{}\n\t{}\n</manifest>".format(comment.toxml(), node_xml))

    # merge application level nodes
    for tag in ["meta-data", "activity", "service", "receiver", "provider"]:
        for node in get_xml_elements(src_application, tag):
            node_xml = node.toxml().replace("${applicationId}", "{{android.package}}")
            if node_xml not in dst_manifest:
                dst_manifest = dst_manifest.replace("</application>", "\t{}\n\t\t{}\n\t</application>".format(comment.toxml(), node_xml))

    # write prettified xml to file
    with open(dst_manifest_name, "w") as dst_file:
        dst_file.write(dst_manifest)


@contextmanager
def tmpdir():
    name = tempfile.mkdtemp()
    try:
        yield name
    finally:
        shutil.rmtree(name)


def unzip(filename, destination):
    print("Unpacking {}".format(filename))
    zip_ref = zipfile.ZipFile(filename, 'r')
    zip_ref.extractall(destination)
    zip_ref.close()


def add_to_zip(zipfile_name, file_to_add, path_in_zip):
    zip_ref = zipfile.ZipFile(zipfile_name, 'a')
    zip_ref.write(file_to_add, path_in_zip)
    zip_ref.close()


def download_file(url, destination):
    filename = os.path.join(destination, url.rsplit('/', 1)[-1])
    if os.path.exists(filename):
        print("File %s already exists" % (filename))
        sys.exit(1)
    print("Downloading {}".format(url))
    urllib.urlretrieve(url, filename)
    return filename


def download_string(url):
    """ Download data from a URL into a string.
    """
    handle = urllib.urlopen(url)
    return handle.read()


def download_from_builtins(filename, destination):
    stable = download_string("http://d.defold.com/stable/info.json")
    stable_json = json.loads(stable)
    builtins_url = "http://d.defold.com/archive/%s/engine/share/builtins.zip" % (stable_json.get("sha1"))
    with tmpdir() as tmp_dir:
        builtins_file = download_file(builtins_url, tmp_dir)
        unzip(builtins_file, tmp_dir)
        shutil.move(os.path.join(tmp_dir, filename), destination)


def download_android_manifest(destination):
    return download_from_builtins("builtins/manifests/android/AndroidManifest.xml", destination)


def copy_merge(src, dst):
    for name in os.listdir(src):
        src_file = os.path.join(src, name)
        dst_file = os.path.join(dst, name)
        if os.path.exists(dst_file) and os.path.isdir(src_file):
            copy_merge(src_file, dst_file)
        else:
            os.rename(src_file, dst_file)

def find_files(root_dir, file_pattern):
    matches = []
    for root, dirnames, filenames in os.walk(root_dir):
        for filename in fnmatch.filter(filenames, file_pattern):
            matches.append(os.path.join(root, filename))
    return matches


#
# Process an AAR file
# This will unzip it and handle the contents:
# * R.java will get generated from resources
# * Resources will get copied to the output folder
# * classes.jar will get copied to the output folder
# * Manifest stubs wil get merged with the main manifest in the output folder
#
def process_aar(name, aar_file, args, manifest_file):
    with tmpdir() as zip_dir:
        unzip(aar_file, zip_dir)

        # rename resources to unique filenames
        for file in find_files(os.path.join(zip_dir, "res"), "values*.xml"):
            os.rename(file, os.path.join(os.path.dirname(file), name + "-" + os.path.basename(file)))

        r_file = os.path.join(zip_dir, "R.txt")
        if os.path.exists(r_file) and os.path.getsize(r_file) > 0:
            # generate R.java
            manifest_xml = os.path.join(zip_dir, "AndroidManifest.xml")
            res_dir = os.path.join(zip_dir, "res")
            aapt = "${ANDROID_HOME}/build-tools/%s/aapt package --non-constant-id -f -m -M %s -S %s -I ${ANDROID_HOME}/platforms/android-%s/android.jar -J %s" % (args.build_tools_version, manifest_xml, res_dir, args.android_platform_version, zip_dir)
            call(aapt, shell=True)

            # compile R.java and add to classes.jar
            for rjava_file in find_files(zip_dir, "R.java"):
                javac(rjava_file)
                for class_file in find_files(zip_dir, "*.class"):
                    add_to_zip(os.path.join(zip_dir, "classes.jar"), class_file, os.path.relpath(class_file, zip_dir))
        else:
            print("Not generating R.java since dependency has no resources")

        # copy resources
        src_res_dir = os.path.join(zip_dir, "res")
        dst_res_dir = os.path.join(args.out, "res", "android", "res")
        if os.path.exists(src_res_dir):
            dst = os.path.join(dst_res_dir, name + "-" + os.path.basename(aar_file).replace(".aar", ""))
            if not os.path.exists(dst):
                os.makedirs(dst)
            copy_merge(src_res_dir, dst)
            if len(os.listdir(dst) ) == 0:
                os.rmdir(dst)

        # copy classes.jar
        classes_jar = os.path.join(zip_dir, "classes.jar")
        if os.path.exists(classes_jar):
            lib_dir = os.path.join(args.out, "lib", "android")
            classes_jar_dest = os.path.join(args.out, "lib", "android", name + "-" + os.path.basename(aar_file).replace(".aar", ".jar"))
            shutil.move(classes_jar, classes_jar_dest)

        # merge manifest
        android_manifest = os.path.join(zip_dir, "AndroidManifest.xml")
        if os.path.exists(android_manifest):
            merge_manifest_files(android_manifest, manifest_file, name)
            # shutil.copy(android_manifest, os.path.join(".", name + "-AndroidManifest.xml"))


#
# Process a single dependency
# This will download the dependency (.jar or .aar). In the case of an .aar file
# it will get unpacked.
#
def process_dependency(name, url, args, manifest_file):
    print("Processing dependency {} {}".format(name, url))
    with tmpdir() as tmp_dir:
        dependency_file = download_file(url, tmp_dir)
        if dependency_file.endswith(".jar"):
            # copy jar
            lib_dir = os.path.join(args.out, "lib", "android")
            dst_file = os.path.join(lib_dir, name + "-" + os.path.basename(dependency_file))
            if not os.path.exists(dst_file):
                print("Moving %s to %s" % (dependency_file, dst_file))
                shutil.move(dependency_file, dst_file)
        elif dependency_file.endswith(".aar"):
            process_aar(name, dependency_file, args, manifest_file)


#
# Process a list of dependencies
# This will download the dependencies one by one
#
def process_dependencies(dependencies, args):
    print("Downloading and unpacking Android dependencies")

    manifest_file = os.path.join(manifest_dir, "AndroidManifest.xml")
    if os.path.exists(manifest_file):
        os.remove(manifest_file)
    #download_android_manifest(manifest_file)
    create_empty_manifest(manifest_file)

    for name, data in dependencies.iteritems():
        process_dependency(data["group_id"], data["url"], args, manifest_file)


maven_url_cache = {}

#
# Translate a group into a URL
#
def maven_url(group_id, artifact_id, version, extension):
    filename = artifact_id + "-" + version + "." + extension
    if maven_url_cache.get(filename):
        return maven_url_cache.get(filename)

    REPOS = ["https://maven.google.com", "http://central.maven.org/maven2", "http://repo.spring.io/libs-release"]
    for repo in REPOS:
        url = "/".join([repo, group_id.replace(".", "/"), artifact_id, version, filename])
        if urllib.urlopen(url).code == 200:
            maven_url_cache[filename] = url
            return url
    print("Unable to find a url for group {} artifact {) version {} and extension {}".format(url, group_id, artifact_id, version, extension))
    exit(1)


pom_cache = {}

#
# Recurseively download a POM and all its parents
#
def download_pom(pom_url):
    print("Downloading artifact '{}'".format(pom_url))
    if pom_cache.get(pom_url):
        print("  Ignoring artifact '{}' since it has already been downloaded".format(pom_url))
        return

    # download and parse pom
    with tmpdir() as tmp_dir:
        pom_file = download_file(pom_url, tmp_dir)
        xmldoc = minidom.parse(pom_file)

    pom_cache[pom_url] = xmldoc

    # download and parse parent POMs recursively
    project = get_xml_element(xmldoc, "project")
    parent = get_xml_element(project, "parent")
    if parent:
        parent_group_id = get_child_value(parent, "groupId")
        parent_artifact_id = get_child_value(parent, "artifactId")
        parent_version_id = get_child_value(parent, "version")
        parent_pom_url = maven_url(parent_group_id, parent_artifact_id, parent_version_id, "pom")
        print("  Downloading parent artifact '{}'".format(parent_pom_url))
        download_pom(parent_pom_url)


#
# Get an element from a POM
# This will take inheritance into consideration by first looking at any parent POMs
#
def get_pom_element(pom_url, tag_name):
    # some values are never inherited from parent POMs
    NOT_INHERITED = ["artifactId", "name", "prerequisites"]

    xmldoc = pom_cache[pom_url]
    project = get_xml_element(xmldoc, "project")

    element = get_child_element(project, tag_name)
    if element:
        return element
    elif tag_name in NOT_INHERITED:
        return default

    parent = get_xml_element(project, "parent")
    if parent:
        parent_group_id = get_child_value(parent, "groupId")
        parent_artifact_id = get_child_value(parent, "artifactId")
        parent_version_id = get_child_value(parent, "version")
        parent_pom_url = maven_url(parent_group_id, parent_artifact_id, parent_version_id, "pom")
        return get_pom_element(parent_pom_url, tag_name)
    else:
        return None

#
# Get a value from a POM
# This will take inheritance into consideration by first looking at any parent POMs
#
def get_pom_value(pom_url, tag_name, default=None):
    value = get_element_value(get_pom_element(pom_url, tag_name))
    if value:
        return value
    else:
        return default

#
# Recursivley process POM files adding each to the output dictionary
#
def process_pom(pom_url, dependencies_out):
    # Replace a template value ${foo} with the actual value read from a list of properties
    def replace_property(value, properties):
        if value and value.startswith("${"):
            value = value.replace("${", "").replace("}", "")
            value = get_child_value(properties, value)
        return value

    # Get the version tag value from an element
    def get_version(element):
        version = get_child_value(element, "version")
        if version:
            version = version.replace("[", "").replace("]", "").split(",", 1)[0]
        return version

    # Get the version of this pom (will traverse parents)
    def get_project_version():
        return get_pom_value(pom_url, "version")

    download_pom(pom_url)

    properties = get_pom_element(pom_url, "properties")
    group_id = get_pom_value(pom_url, "groupId")
    artifact_id = get_pom_value(pom_url, "artifactId")
    packaging = get_pom_value(pom_url, "packaging", "jar")
    version = replace_property(get_project_version(), properties)
    url = maven_url(group_id, artifact_id, version, packaging)
    group_formatted = group_id.replace(".", "-")
    dependency_id = group_formatted + "-" + artifact_id
    if dependencies_out.get(dependency_id):
        print("  Ignoring artifact '{}' since it has already been processed".format(dependency_id))
        return
    dependencies_out[dependency_id] = {"url":url, "group_id":group_formatted}

    # process artifact dependencies
    dependencies = get_pom_element(pom_url, "dependencies")
    if dependencies:
        for dependency in get_xml_elements(dependencies, "dependency"):
            dependency_artifact_id = get_child_value(dependency, "artifactId")
            dependency_scope = get_child_value(dependency, "scope")
            if dependency_scope and dependency_scope != "test":
                print("  Including artifact dependency '{}' with scope '{}'".format(dependency_artifact_id, dependency_scope))
                dependency_group_id = get_child_value(dependency, "groupId")
                dependency_version = replace_property(get_version(dependency), properties) or version
                dependency_pom_url = maven_url(dependency_group_id, dependency_artifact_id, dependency_version, "pom")
                process_pom(dependency_pom_url, dependencies_out)
            else:
                print("  Ignoring artifact dependency '{}' with scope '{}'".format(dependency_artifact_id, dependency_scope))


#
# Process a list of POMs
#
def process_poms(poms):
    print("Downloading and processing POMs", poms)
    dependencies = {}
    for pom in poms:
        process_pom(pom, dependencies)
    return dependencies


def add_argument(parser, short, long, dest, help, default=None, required=False, action="store"):
    parser.add_argument(short, dest=dest, help=help, default=default, required=required, action=action)
    parser.add_argument(long, dest=dest, help=help, default=default, required=required, action=action)


parser = ArgumentParser()
parser.add_argument('commands', nargs="+", help='Commands (poms, deps, plist, help)')
add_argument(parser, "-o", "--out", "out", "Path to generate files in", default="out")
add_argument(parser, "-d", "--deps", "deps", "Filename to read/write dependencies json from", default="dependencies.json")
add_argument(parser, "-p", "--pom", "poms", "Path to POM file to process. For use with the 'poms' command.", action="append")
add_argument(parser, "-btv", "--build-tools-version", "build_tools_version", "Android build tools version. Optional, for use with 'deps' command.", default="28.0.2")
add_argument(parser, "-apv", "--android-platform-version", "android_platform_version", "Android platform version. Optional, for use with 'deps' command.", default="26")
add_argument(parser, "-pl", "--plist", "google_services_plist", "GoogleService-Info.plist as downloaded from Firebase Console. Optional, for use with 'plist' command.", default="GoogleService-Info.plist")
args = parser.parse_args()

help = """
COMMANDS:
poms = [Android] Process POMs. This will download, parse and generate a list of all dependencies (direct and transitive) to the file specified by [-d|--deps].

deps = [Android] Process dependencies. This will parse the file specified by [-d|--deps], download the .aar or .jar files, copy resources and generate an AndroidManifest.xml.
"""

if not os.path.exists(args.out):
    os.makedirs(args.out)

lib_dir = os.path.join(args.out, "lib", "android")
if not os.path.exists(lib_dir):
    os.makedirs(lib_dir)

manifest_dir = os.path.join(args.out, "manifests", "android")
if not os.path.exists(manifest_dir):
    os.makedirs(manifest_dir)

res_dir = os.path.join(args.out, "res", "android", "res")
if not os.path.exists(res_dir):
    os.makedirs(res_dir)


deps_file = os.path.join(args.out, args.deps)

for command in args.commands:
    if command == "help":
        parser.print_help()
        print(help)
        sys.exit(0)

    if command == "poms":
        with open(deps_file, "w") as file:
            file.write(json.dumps(process_poms(args.poms)))

    if command == "deps":
        if not os.path.exists(deps_file):
            print("File %s does not exist" % (deps_file))
            sys.exit(1)
        with open(deps_file, "r") as file:
            dependencies = json.loads(file.read())
            process_dependencies(dependencies, args)

# Success!
print("Done")
