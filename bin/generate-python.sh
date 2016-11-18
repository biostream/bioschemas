#!/bin/bash
# use protoc to create python code
# see https://developers.google.com/protocol-buffers/

#### NOT USED
# export PY_OUT=../bioschemas/snapshot/python
# rm -r $PY_OUT
# mkdir $PY_OUT
# PROTO_PATH=../schemas/bmeg/ohsu/schema
# mkdir -p $PY_OUT/bmeg
# protoc --proto_path=$PROTO_PATH \
#   --python_out=$PY_OUT/bmeg\
#   $PROTO_PATH/*.proto
# echo "code generated into $PY_OUT/bmeg"
#
#
# PROTO_PATH=../bioschemas/ga4gh/src/main/proto
# mkdir -p $PY_OUT/ga4gh
# protoc  --proto_path=$PROTO_PATH \
#         --python_out=$PY_OUT/ga4gh  \
#         $PROTO_PATH/ga4gh/*
# echo "code generated into $PY_OUT/ga4gh"
