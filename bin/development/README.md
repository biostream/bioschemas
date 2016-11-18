# Development

The protoc plugin architecture makes it difficult to use debuggers and other tools.
The `my-capture-plugin.py` simply pipes the input from protoc to stderr so that it
can be captured and used in the development process.

e.g
```
$ protoc --plugin=protoc-gen-custom=development/my-capture-plugin.py     --proto_path=../proto/ --custom_out=$JS_OUT  ../proto/ccc/resource.proto 2> development/my-capture.data
...
$ ipython custom-plugin.py  development/my-capture.data
```
