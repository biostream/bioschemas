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




## utilty
The ga4gh and bmeg cannonical schemas are maintained in protobuf.  The `bin/custom-plugin.py` processes the schemas for alternate uses (jsonschema, cerebus).  _The `bioschemas/snapshot` directory contains output from protoc.
  Please do not hand edit, rather change `custom-plugin.py` or `json-to-cerberus.py`_
