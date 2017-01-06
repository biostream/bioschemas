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

# use bioschemas git hash as hash of icgc-dcc, since icgc-dcc is not in a
# separate repository.
icgc_dcc = bioschemas

d = datetime.datetime.utcnow()

print json.dumps({'bioschemas': bioschemas,
                  'ga4gh': ga4gh,
                  'bmeg': bmeg,
                  'gdc': gdc,
                  'ohsu': bioschemas,
                  'icgc-dcc': bioschemas,
                  'created_at': d.isoformat("T") + "Z"
                  })
