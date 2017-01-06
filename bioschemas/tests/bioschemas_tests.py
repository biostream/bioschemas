#!/usr/bin/env python

from unittest import TestCase
import bioschemas
import json
import jsonschema
from jsonschema.exceptions import SchemaError
from os.path import dirname, isdir, abspath, join, exists, realpath


def test_should_return_path():
    assert bioschemas.schema_path()


def test_paths_should_have_proto():
    assert isdir(abspath(join(bioschemas.schema_path(), "proto")))
    assert isdir(abspath(join(bioschemas.schema_path(), "proto/bmeg")))
    assert isdir(abspath(join(bioschemas.schema_path(), "proto/ga4gh")))


def test_should_jsonschema():
    assert bioschemas.json_schema('Resource')


def test_should_cerberus_schema():
    assert bioschemas.cerberus_schema('Resource')


def test_should_return_git_hashes():
    h = bioschemas.git_hashes()
    assert h
    assert 'bmeg' in h
    assert 'ga4gh' in h
    assert 'gdc' in h
    assert 'icgc-dcc' in h


def test_should_have_gdc_submission_templates():
    assert bioschemas.gdc_submission_templates()


def test_should_return_submission_template_by_type():
    assert bioschemas.gdc_submission_template('file')


def test_file_centric_is_valid():
    schema = bioschemas.json_schema('file-centric')
    try:
        jsonschema.Draft4Validator.check_schema(schema)
    except SchemaError as e:
        assert False, 'schema error'


def test_file_centric_validation():
    test_path = dirname(realpath(__file__))
    schema = bioschemas.json_schema('file-centric')
    with open(join(test_path, 'example-file-centric.json'), 'rb') as rd:
        jsonschema.validate(json.load(rd), schema)

