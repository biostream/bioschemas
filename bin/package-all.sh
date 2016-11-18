#!/bin/bash

# generate  snapshot
./copy-proto.sh
./generate-cerberus.sh
./generate-jsonschema.sh

python git_hashes.py > ../bioschemas/snapshot/git_hashes.json
# test it
cd ..
python setup.py test
