#!/usr/bin/env python

"""
make the gdc templates easier to consume
(convert from array to hash)
"""
import sys
import json

template_array = json.loads(sys.stdin.read())

templates = {}
for template in template_array:
    templates[template['type']] = template

print json.dumps(templates, indent=2)
