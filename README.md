# pompom
Process POM files for use in Defold Native Extensions

This is a tool with two purposes:

1. Given one or more POM files it will generate a list of dependencies, including transitive dependencies.
2. Given a list of dependencies it will download each of them and in the case of AAR files also unpack and compile resources and merge manifest stubs

## Requirements
You need the following tools:

* Android Build Tools (specifically aapt to generate R.java)
* Java (to compile generated R.java)

## Usage
Refer to any of the bash script in the root of the project. There are scripts to generate the needed files for Google Play Services, Google Play Game Services, Facebook and more.

## Notes
Manifest merging is done using a standalone version of the Android Manifest Merger tool:

* https://github.com/Bresiu/android-manifest-merger

## Useful links
* https://mvnrepository.com/
