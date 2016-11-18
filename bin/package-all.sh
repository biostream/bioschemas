#!/bin/bash

# generate  snapshot
./copy-proto.sh
./generate-cerberus.sh
./generate-jsonschema.sh

python git_hashes.py > ../bioschemas/snapshot/git_hashes.json
cp ./SNAPSHOT-README.md ../bioschemas/snapshot/README.md
curl -s 'https://gdc-api.nci.nih.gov/v0/submission/template/?format=json' \
 | python pre_process_gdc_template.py > ../bioschemas/snapshot/gdc_submission_templates.json

# test it
cd ..
python setup.py test
