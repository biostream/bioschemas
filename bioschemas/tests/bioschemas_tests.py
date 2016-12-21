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
    assert isdir(abspath(join(bioschemas.schema_path(), "proto/ohsu")))


def test_should_jsonschema():
    assert bioschemas.json_schema('Resource')


def test_should_cerberus_schema():
    assert bioschemas.cerberus_schema('Resource')


def test_should_return_git_hashes():
    assert bioschemas.git_hashes()


def test_should_have_gdc_submission_templates():
    assert bioschemas.gdc_submission_templates()


def test_should_return_submission_template_by_type():
    assert bioschemas.gdc_submission_template('file')

