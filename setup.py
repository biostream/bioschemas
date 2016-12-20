#!/usr/bin/env python

from setuptools import setup, find_packages

setup(name='Bioschemas',
      version='1.0',
      description='OHSU Bio Schemas',
      author='Brian Walsh',
      author_email='walsbr@ohsu.edu',
      include_package_data=True,
      url='https://github.com/ohsu-computational-biology/bioschemas',  # nopep8
      packages=find_packages(),
      install_requires=[
          'jsonschema',
          'protobuf'
      ],
      test_suite='nose.collector',
      tests_require=['nose'],
      scripts=['bioschemas/bin/bioschemas-snapshot'],
)
