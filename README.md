# bioschemas

Common data structures and APIs.

This repo contains
* git submodules from [ga4gh](https://github.com/ga4gh/schemas), [gdc](https://github.com/NCI-GDC/gdcdictionary) and [bmeg](https://github.com/bmeg/bmeg-schemas)
* A utility to read the schemas and produce different output (jsonschema and cerberus)

## packaging
The schemas are packaged into a python module `bioschemas`
The justification for the packaging is threefold:
* Moves complexities of gitmodule management from the end user to the package release process
* Each of the submodules referenced have many other components other than the schemas themselves.  Packaging allows us to trim all components other than schema source.
* The generated snapshot _is checked into git_ - the rationalization is that is allows us to tag package explicitly and allows clients to install the package without submodule complexity.

```
pip install git+https://github.com/ohsu-computational-biology/bioschemas
```

### package release

```
cd bin
./package-all.sh
 ... generates schema snapshot ...
 ... runs setup tests ...
----------------------------------------------------------------------
Ran 4 tests in 0.100s

OK
```

### usage
```
$ bioschemas-snapshot --help
usage: bioschemas-snapshot [-h] [-o OUTPUT] [-v]

Extract bioschemas schema directory [ga4gh,bmeg,gdc]

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        Extract to this directory name. Must not already
                        exist; it will be created as well as missing parent
                        directories.
  -v, --version         Print git hashes
```

### python usage

```
import  bioschemas

bioschemas.schema_path()
>> '/home/someuser/bioschemas/bioschemas/snapshot'


 bioschemas.json_schema('Resource')
>> '{"type": "object", "properties": {"mimeType": {"type": "string"}, "info": {"type": "object"}, "name": {"type": "string"}, "format": {"type": "string"}, "checksum": {"type": "string"}, "description": {"type": "string"}, "created": {"type": "string"}, "class": {"type": "string"}, "gid": {"type": "string"}, "location": {"type": "string"}, "type": {"type": "string"}, "id": {"type": "string"}, "datasetID": {"type": "string"}, "size": {"type": "integer"}}}'

 bioschemas.cerberus_schema('Resource')
>>  '{"mimeType": {"type": "string"}, "info": {"type": {"type": "dict"}}, "name": {"type": "string"}, "format": {"type": "string"}, "checksum": {"type": "string"}, "description": {"type": "string"}, "created": {"type": "string"}, "class": {"type": "string"}, "gid": {"type": "string"}, "location": {"type": "string"}, "type": {"type": "string"}, "id": {"type": "string"}, "datasetID": {"type": "string"}, "size": {"type": "integer"}}'

bioschemas.git_hashes()
>>  '{"bioschemas": "067b1d2", "created_at": "2016-11-18T04:58:19.593297Z", "gdc": "288f042", "bmeg": "537f94a"}'

```

The snapshot can be used by any language context and has the following structure:
```
.
├── cerberus
│   ├── bmeg
│   ├── ga4gh
│   │   ├── ga4gh
│   │   └── google
│   │       ├── api
│   │       └── protobuf
│   └── gdc
├── jsonschema
│   ├── bmeg
│   ├── ga4gh
│   │   ├── ga4gh
│   │   └── google
│   │       ├── api
│   │       └── protobuf
│   └── gdc
└── proto
    ├── bmeg
    └── ga4gh
        ├── ga4gh
        └── google
            └── api
```




## utilty
The ga4gh and bmeg cannonical schemas are maintained in protobuf.  The `bin/custom-plugin.py` processes the schemas for alternate uses (jsonschema, cerebus).  _The `bioschemas/snapshot` directory contains output from protoc.
  Please do not hand edit, rather change `custom-plugin.py` or `json-to-cerberus.py`_
