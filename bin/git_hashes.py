import subprocess
import os
import json
import datetime


def get_git_revision_short_hash():
    return subprocess.check_output(
                ['git', 'rev-parse', '--short', 'HEAD']).strip()


os.chdir('..')
bioschemas = get_git_revision_short_hash()

os.chdir('schemas/bmeg')
bmeg = get_git_revision_short_hash()

os.chdir('../ga4gh')
ga4gh = get_git_revision_short_hash()

os.chdir('../gdc')
gdc = get_git_revision_short_hash()

d = datetime.datetime.utcnow()

print json.dumps({'bioschemas': bioschemas,
                  'bmeg': bmeg,
                  'gdc': gdc,
                  'created_at': d.isoformat("T") + "Z"
                  })
