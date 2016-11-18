#!/bin/bash

export PROTO_OUT=../bioschemas/snapshot/proto
rm -r $PROTO_OUT

mkdir $PROTO_OUT
PROTO_PATH=../schemas/bmeg/ohsu/schema
mkdir -p $PROTO_OUT/bmeg
cp -r  $PROTO_PATH/*.proto  $PROTO_OUT/bmeg
echo "proto copied into $PROTO_OUT/bmeg"


PROTO_PATH=../schemas/ga4gh/src/main/proto
mkdir -p $PROTO_OUT/ga4gh
cp -r  $PROTO_PATH/*  $PROTO_OUT/ga4gh
echo "proto copied into $PROTO_OUT/ga4gh"
