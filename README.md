# pompom
Process POM files for use in Defold Native Extensions

This is a tool with two purposes:

1. Given one or more POM files it will generate a list of dependencies, including transitive dependencies.
2. Given a list of dependencies it will download each of them and in the case of AAR files also unpack and compile resources and merge manifest stubs
