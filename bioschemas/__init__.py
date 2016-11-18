#!/usr/bin/env python

""" provide schemas """

import fnmatch
import glob
import json
import jsonschema
import os
import sys

# complete jsonschemas
json_schemas = {'definitions': {}}
cerberus_schemas = {'domains': {}}
gdc_templates = {}


def _init():
    definitions = json_schemas['definitions']

    # load all schema fragments
    path = os.path.join(os.path.dirname(__file__), "snapshot/jsonschema")

    schema_files = [os.path.join(dirpath, f)
                    for dirpath, dirnames, files in os.walk(path)
                    for f in fnmatch.filter(files, '*.json')]

    for schema_file in schema_files:
        with open(schema_file) as file_object:
            fragment = json.load(file_object)
            for key in fragment['definitions'].keys():
                definitions[key] = fragment['definitions'][key]

    # check the schema to ensure all OK
    # jsonschema.Draft4Validator.check_schema(json_schemas)

    domains = cerberus_schemas['domains']

    # load all schema fragments
    path = os.path.join(os.path.dirname(__file__), "snapshot/cerberus")

    schema_files = [os.path.join(dirpath, f)
                    for dirpath, dirnames, files in os.walk(path)
                    for f in fnmatch.filter(files, '*.json')]

    for schema_file in schema_files:
        with open(schema_file) as file_object:
            fragment = json.load(file_object)
            for key in fragment['DOMAIN'].keys():
                domains[key] = fragment['DOMAIN'][key]
    global gdc_templates
    gdc_templates = json.loads(gdc_submission_templates())


def json_schema(key):
    """
    return a json_schemas dict of a given schema
    """
    return json_schemas['definitions'][key]


def cerberus_schema(key):
    """
    return a cerberus dict of a given schema
    """
    return cerberus_schemas['domains'][key]


def schema_path():
    """
    return the path of schemas within package
    """
    return os.path.abspath(os.path.join(os.path.dirname(__file__), "snapshot"))


def git_hashes():
    """
    return git hashes at time of snapshot
    """
    path = os.path.join(os.path.dirname(__file__), "snapshot/git_hashes.json")
    with open(path, "r") as myfile:
        return myfile.read().strip()


def gdc_submission_templates():
    """
    return json string of templates
    """
    path = os.path.join(os.path.dirname(__file__),
                        "snapshot/gdc_submission_templates.json")
    with open(path, "r") as myfile:
        return myfile.read().strip()


def gdc_submission_template(type):
    """
    return dict of template for a given type
    """
    return gdc_templates[type]


# load all
_init()
