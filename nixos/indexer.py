"""
TODO
"""
from whoosh.index import create_in
from whoosh.fields import *
schema = Schema(
    name=TEXT(stored=True),
    version=TEXT(stored=True),
    pname=TEXT(stored=True),
    available=BOOLEAN(stored=True),
    broken=BOOLEAN(stored=True),
    insecure=BOOLEAN(stored=True),
    unfree=BOOLEAN(stored=True),
    unsupported=BOOLEAN(stored=True),
    description=TEXT(stored=True),
    homepage=ID(stored=True),
    license_shortName=TEXT(stored=True),
    maintainers_name=NGRAM(stored=True),
    maintainers_github=TEXT(stored=True),
    platforms=TEXT(stored=True),
    position=ID(stored=True)
)
