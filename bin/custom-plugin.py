#!/usr/bin/env python

"""
protoc plugin to render jsonschema & cerebus documents
"""
import itertools
import json
import os
import sys

from collections import OrderedDict

from google.protobuf.compiler import plugin_pb2 as plugin
from google.protobuf.descriptor_pb2 import DescriptorProto, EnumDescriptorProto
from google.protobuf import descriptor_pb2


# mapping
TYPE = {
  'STRING': descriptor_pb2.FieldDescriptorProto.TYPE_STRING,
  'DOUBLE': descriptor_pb2.FieldDescriptorProto.TYPE_DOUBLE,
  'FLOAT': descriptor_pb2.FieldDescriptorProto.TYPE_FLOAT,
  'INT32': descriptor_pb2.FieldDescriptorProto.TYPE_INT32,
  'SINT32': descriptor_pb2.FieldDescriptorProto.TYPE_SINT32,
  'UINT32': descriptor_pb2.FieldDescriptorProto.TYPE_UINT32,
  'INT64': descriptor_pb2.FieldDescriptorProto.TYPE_INT64,
  'SINT64': descriptor_pb2.FieldDescriptorProto.TYPE_SINT64,
  'UINT64': descriptor_pb2.FieldDescriptorProto.TYPE_UINT64,
  'MESSAGE': descriptor_pb2.FieldDescriptorProto.TYPE_MESSAGE,
  'BYTES': descriptor_pb2.FieldDescriptorProto.TYPE_BYTES,
  'BOOL': descriptor_pb2.FieldDescriptorProto.TYPE_BOOL,
  'ENUM': descriptor_pb2.FieldDescriptorProto.TYPE_ENUM,
  # TODO: More types.
}

# reverse mapping
STRING_TYPE = {
 descriptor_pb2.FieldDescriptorProto.TYPE_STRING:  'string'				,
 descriptor_pb2.FieldDescriptorProto.TYPE_DOUBLE:  'number'				,
 descriptor_pb2.FieldDescriptorProto.TYPE_FLOAT:  'number'				,
 descriptor_pb2.FieldDescriptorProto.TYPE_INT32:  'integer'				,
 descriptor_pb2.FieldDescriptorProto.TYPE_SINT32:  'integer'				,
 descriptor_pb2.FieldDescriptorProto.TYPE_UINT32:  'integer'				,
 descriptor_pb2.FieldDescriptorProto.TYPE_INT64:  'integer'				,
 descriptor_pb2.FieldDescriptorProto.TYPE_SINT64:  'integer'				,
 descriptor_pb2.FieldDescriptorProto.TYPE_UINT64:  'integer'				,
 descriptor_pb2.FieldDescriptorProto.TYPE_MESSAGE:  'object'			,
 descriptor_pb2.FieldDescriptorProto.TYPE_BYTES:  'BYTES'				,
 descriptor_pb2.FieldDescriptorProto.TYPE_BOOL:  'boolean'					,
 descriptor_pb2.FieldDescriptorProto.TYPE_ENUM:  'ENUM'					,
 0: 'null'
}


# see
# http://www.expobrain.net/2015/09/13/create-a-plugin-for-google-protocol-buffer
def traverse(proto_file):
    """ recurse down through the schema. yield item, package """
    def _traverse(package, items):
        for item in items:
            yield item, package

            if isinstance(item, DescriptorProto):
                for enum in item.enum_type:
                    yield enum, package

                nested_package = package + item.name
                for nested in item.nested_type:
                    for (nested_item, nested_package) in _traverse(
                                                            nested_package,
                                                            [nested]):
                        yield nested_item, nested_package

    return itertools.chain(
        _traverse(proto_file.package, proto_file.enum_type),
        _traverse(proto_file.package, proto_file.message_type),
    )


def simplify_input(request, type_formatter):
    """
    given a request, simplify the input provided by protoc.
    the type_formatter styles embedded objects.
    recurse compiler input, create intermediate, simpler structure.
    """
    for proto_file in request.proto_file:
        output = []
        # Parse request
        for item, package in traverse(proto_file):
            if isinstance(item, tuple):
                # sys.stderr.write("skip {} {} {}\n".format(item[0],
                #                                           item[0].__class__,
                #                                           item[1].__class__))
                continue
            else:
                data = {
                    'package': proto_file.package or '&lt;root&gt;',
                    'filename': proto_file.name,
                    'name': item.name
                }

            if isinstance(item, DescriptorProto):
                item.field.sort(key=lambda x: x.number)
                # sys.stderr.write("{}\n".format(item.name))
                # for f in item.field:
                #     sys.stderr.write("  {} {} \n".format(f.name, f.number))
                data.update({
                    'type': 'Message',
                    'properties': [{'name': f.name,
                                    'type': int(f.type),
                                    'type_name': type_formatter(f),
                                    'number': f.number}
                                   for f in item.field]
                })
                if item.nested_type:
                    for nt in item.nested_type:
                        extradata = {
                            'package': proto_file.package or '&lt;root&gt;',
                            'filename': proto_file.name,
                            'name': "{}.{}.{}".format(proto_file.package,
                                                      item.name,
                                                      nt.name),
                            'nested_type': True
                        }
                        nt.field.sort(key=lambda x: x.number)
                        extradata.update({
                            'type': 'Message',
                            'properties': [{'name': f.name,
                                            'type': int(f.type),
                                            'type_name': type_formatter(f),
                                            'number': f.number}
                                           for f in nt.field]
                        })
                        output.append(extradata)

            elif isinstance(item, EnumDescriptorProto):
                data.update({
                    'type': 'Enum',
                    'values': [{'name': v.name, 'value': v.number}
                               for v in item.value]
                })
            output.append(data)
        yield proto_file, output


def generate_cerberus(request, response):
    """
    given input from compiler, generate response back to compiler.
    use simplify_input's structure to generate cerberus
    """
    def _toTypeName(f):
        """ simplify, embedded types are dicts """
        if f.type_name:
            return {"type": "dict"}
        return STRING_TYPE[int(f.type)]

    for proto_file, output in simplify_input(request, _toTypeName):
        # Fill response
        cerberus = {"DOMAIN": {}}
        domains = cerberus["DOMAIN"]
        for data in output:
            # simplify for cerberus, do not include nested
            if 'nested_type' in data:
                continue
            o = OrderedDict()
            if "properties" in data:
                for property in data["properties"]:
                        o[property['name']] = {
                            'type': property['type_name']
                        }
            elif "values" in data:
                for value in data["values"]:
                        o[value['name']] = {
                            'type': value['value']
                        }
            else:
                sys.stderr.write(
                    "did not parse because, no properties or values: {}\n"
                    .format(str(data)))

            domains[data['name']] = o

        f = response.file.add()
        f.name = proto_file.name + '.json'
        f.content = json.dumps(cerberus, indent=2)


def generate_jsonschema(request, response):
    """
    given input from compiler, generate response back to compiler.
    use simplify_input's structure to generate json schema
    """
    def _toTypeNameRigorous(f):
        """ rigorous, embedded types are references """
        if f.type_name:
            return {"$ref": "#{}".format(f.type_name)}
        return STRING_TYPE[int(f.type)]

    def _toTypeNameSimple(f):
        """ simplify, embedded types are objects """
        if f.type_name:
            return "object"
        return STRING_TYPE[int(f.type)]

    for proto_file, output in simplify_input(request, _toTypeNameSimple):
        # Fill response
        jsonschema = {"definitions": {}}
        definitions = jsonschema["definitions"]
        for data in output:
            o = {
                "type": "object",
                "properties": OrderedDict({})
            }
            if "properties" in data:
                # # maintain protobuf number order
                # data['properties'].sort(key=lambda f: f['number'])
                for property in data["properties"]:
                        o['properties'][property['name']] = {
                            'type': property['type_name']
                        }
            elif "values" in data:
                for value in data["values"]:
                        o['properties'][value['name']] = {
                            'type': value['value']
                        }
            else:
                sys.stderr.write(
                    "did not parse because, no properties or values: {}\n"
                    .format(str(data)))

            definitions[data['name']] = o

        f = response.file.add()
        f.name = proto_file.name + '.json'
        f.content = json.dumps(jsonschema, indent=2)

# protoc --plugin=protoc-gen-custom=custom-plugin.py \
#  --custom_out=./build hello.proto
if __name__ == '__main__':
    # Read request message from stdin, or file (file used for development)
    with open(sys.argv[1], 'r') if len(sys.argv) > 1 else sys.stdin as f:
        data = f.read()
    # Parse request
    request = plugin.CodeGeneratorRequest()
    request.ParseFromString(data)

    # Create response
    response = plugin.CodeGeneratorResponse()

    # Generate code
    if 'PROTO_TO_JSONSCHEMA' in os.environ:
        generate_jsonschema(request, response)
    elif 'PROTO_TO_CERBERUS' in os.environ:
        generate_cerberus(request, response)

    # Serialise response message
    output = response.SerializeToString()

    # Write to stdout
    sys.stdout.write(output)
