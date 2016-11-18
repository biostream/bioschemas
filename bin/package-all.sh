#!/bin/bash

# generate  snapshot
./copy-proto.sh
./generate-cerberus.sh
./generate-jsonschema.sh

# test it
cd ..
python setup.py test
