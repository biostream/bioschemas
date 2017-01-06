#!/bin/bash
# use protoc to create cerebus friendly json code

# since we cannot pass flags to our plugin, we use env vars.
# the PROTO_TO_CERBERUS var controlls both what type of output to generate
# and where to put it

export PROTO_TO_CERBERUS=../bioschemas/snapshot/cerberus
rm -r $PROTO_TO_CERBERUS
mkdir $PROTO_TO_CERBERUS
PROTO_PATH=../schemas/ohsu
mkdir -p $PROTO_TO_CERBERUS/ohsu
protoc --plugin=protoc-gen-custom=custom-plugin.py \
       --proto_path=$PROTO_PATH \
       --custom_out=$PROTO_TO_CERBERUS/ohsu \
       $PROTO_PATH/*.proto
echo "cerberus code snapshot into $PROTO_TO_CERBERUS/ohsu"


PROTO_PATH=../schemas/ga4gh/src/main/proto
mkdir -p $PROTO_TO_CERBERUS/ga4gh
protoc --plugin=protoc-gen-custom=custom-plugin.py \
       --proto_path=$PROTO_PATH \
       --custom_out=$PROTO_TO_CERBERUS/ga4gh \
       $PROTO_PATH/ga4gh/*
echo "cerberus code snapshot into $PROTO_TO_CERBERUS/ga4gh"

mkdir -p $PROTO_TO_CERBERUS/gdc
python json-to-cerberus.py > $PROTO_TO_CERBERUS/gdc/schema.json
echo "cerberus code moved into $PROTO_TO_CERBERUS/gdc"
