#!/usr/bin/env python

from unittest import TestCase
import bioschemas
from os.path import isdir, abspath, join, exists


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
