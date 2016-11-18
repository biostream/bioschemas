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


### python usage

```
import  bioschemas

bioschemas.schema_path()
>> '/home/someuser/bioschemas/bioschemas/snapshot'

 bioschemas.json_schema('Resource')
>> {u'properties': {u'checksum': {u'type': u'string'}, u'class': {u'type': u'string'}, u'created': {u'type': u'string'}, u'datasetID': {u'type': u'string'}, u'description': {u'type': u'string'}, u'format': {u'type': u'string'}, u'gid': {u'type': u'string'}, u'id': {u'type': u'string'}, u'info': {u'type': u'object'}, u'location': {u'type': u'string'}, u'mimeType': {u'type': u'string'}, u'name': {u'type': u'string'}, u'size': {u'type': u'integer'}, u'type': {u'type': u'string'}}, u'type': u'object'}  

 bioschemas.cerberus_schema('Resource')
>> {u'checksum': {u'type': u'string'}, u'class': {u'type': u'string'}, u'created': {u'type': u'string'}, u'datasetID': {u'type': u'string'}, u'description': {u'type': u'string'}, u'format': {u'type': u'string'}, u'gid': {u'type': u'string'}, u'id': {u'type': u'string'}, u'info': {u'type': {u'type': u'dict'}}, u'location': {u'type': u'string'}, u'mimeType': {u'type': u'string'}, u'name': {u'type': u'string'}, u'size': {u'type': u'integer'}, u'type': {u'type': u'string'}}

bioschemas.git_hashes()
>>  {u'bioschemas': u'f40f653', u'bmeg': u'537f94a', u'created_at': u'2016-11-18T17:47:56.858397Z', u'gdc': u'288f042'}

bioschemas.gdc_submission_template('file')

>> {u'aliquots': {u'submitter_id': None}, u'analytes': {u'submitter_id': None}, u'archives': {u'submitter_id': None}, u'cases': {u'submitter_id': None}, u'centers': {u'code': None}, u'data_formats': {u'name': None}, u'data_subtypes': {u'name': None}, u'derived_files': {u'submitter_id': None}, u'described_cases': {u'submitter_id': None}, u'experimental_strategies': {u'name': None}, u'file_name': None, u'file_size': None, u'md5sum': None, u'platforms': {u'name': None}, u'portions': {u'submitter_id': None}, u'project_id': None, u'related_files': {u'submitter_id': None}, u'samples': {u'submitter_id': None}, u'slides': {u'submitter_id': None}, u'state_comment': None, u'submitter_id': None, u'tags': {u'name': None}, u'type': u'file'}
```




## utilty
The ga4gh and bmeg cannonical schemas are maintained in protobuf.  The `bin/custom-plugin.py` processes the schemas for alternate uses (jsonschema, cerebus).  _The `bioschemas/snapshot` directory contains output from protoc.
  Please do not hand edit, rather change `custom-plugin.py` or `json-to-cerberus.py`_
