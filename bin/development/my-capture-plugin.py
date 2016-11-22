#!/usr/bin/env python

import sys

# protoc --plugin=protoc-gen-custom=my-capture-plugin.py \
#  --custom_out=./build hello.proto 2> my-capture.data
if __name__ == '__main__':
    # Read request message from stdin
    data = sys.stdin.read()
    sys.stderr.write(data)
