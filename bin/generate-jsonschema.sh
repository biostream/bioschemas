#!/bin/bash
# use protoc to create jsonschema friendly

# since we cannot pass flags to our plugin, we use env vars.
# the PROTO_TO_JSONSCHEMA var controlls both what type of output to generate
# and where to put it

PROTO_PATH=../schemas/bmeg/ohsu

export PROTO_TO_JSONSCHEMA=../bioschemas/snapshot/jsonschema
rm -r $PROTO_TO_JSONSCHEMA
mkdir $PROTO_TO_JSONSCHEMA
PROTO_PATH=../schemas/bmeg/ohsu/schema
mkdir -p $PROTO_TO_JSONSCHEMA/bmeg
protoc --plugin=protoc-gen-custom=custom-plugin.py \
       --proto_path=$PROTO_PATH \
       --custom_out=$PROTO_TO_JSONSCHEMA/bmeg \
       $PROTO_PATH/*.proto
echo "jsonschema code generated into $PROTO_TO_JSONSCHEMA/bmeg"


PROTO_PATH=../schemas/ga4gh/src/main/proto
mkdir -p $PROTO_TO_JSONSCHEMA/ga4gh
protoc --plugin=protoc-gen-custom=custom-plugin.py \
       --proto_path=$PROTO_PATH \
       --custom_out=$PROTO_TO_JSONSCHEMA/ga4gh \
       $PROTO_PATH/ga4gh/*
echo "jsonschema code generated into $PROTO_TO_JSONSCHEMA/ga4gh"

# gdc already in json schemas
mkdir -p $PROTO_TO_JSONSCHEMA/gdc
python -c '
import sys
from json import dumps
sys.path.append("../schemas/gdc/gdcdictionary")
from python import gdcdictionary
d = {"definitions": gdcdictionary.schema}
print dumps(d, indent=2)
' > $PROTO_TO_JSONSCHEMA/gdc/schema.json
echo "jsonschema code generated into $PROTO_TO_JSONSCHEMA/gdc"

PROTO_PATH=../schemas/ohsu
mkdir -p $PROTO_TO_JSONSCHEMA/ohsu
protoc --plugin=protoc-gen-custom=custom-plugin.py \
       --proto_path=$PROTO_PATH \
       --custom_out=$PROTO_TO_JSONSCHEMA/ga4gh \
       $PROTO_PATH/ga4gh/*
echo "jsonschema code generated into $PROTO_TO_JSONSCHEMA/ohsu"
