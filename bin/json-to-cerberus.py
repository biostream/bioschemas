#!/usr/bin/env python

import sys
from json import dumps
sys.path.append("../schemas/gdc/gdcdictionary")
from python import gdcdictionary  # NOQA


def to_cerberus(schema):
    cerberus = {"DOMAIN": {}}
    domains = cerberus["DOMAIN"]
    for k in schema.keys():
        o = {}
        clazz = schema[k]
        properties = clazz['properties']
        for property in properties:
            o[property] = _toTypeName(properties[property])
        domains[k] = o
    return cerberus


def _toTypeName(p):
    """ simplify, embedded types are dicts """
    if 'type' not in p:
        return {"type": "dict"}
    if p['type'] == ["string", "null"]:
        return {"type": "string"}
    if p['type'] == ["number", "null"]:
        return {"type": "number"}
    return {"type": p['type']}

cerberus = to_cerberus(gdcdictionary.schema)
print dumps(cerberus, indent=2)
