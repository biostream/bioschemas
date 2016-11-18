
# Bin

Process the proto schemas

`bin/generate-*.sh` wraps the call to protoc.  

usage
```
$ cd bin
$ ./generate-jsonschema.sh
$ ./generate-cereberus.sh
```


## utilty
The ga4gh and bmeg cannonical schemas are maintained in protobuf.  The `bin/custom-plugin.py` processes the schemas for alternate uses (jsonschema, cerebus).
![image](https://cloud.githubusercontent.com/assets/47808/19787247/a21d16fe-9c56-11e6-9f2e-523c43653607.png)
