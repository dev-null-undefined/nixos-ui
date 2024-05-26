"""
TODO
"""
import os

from whoosh.filedb.filestore import FileStorage
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
    license_short_name=TEXT(stored=True),
    maintainers_name=NGRAM(stored=True),
    maintainers_github=TEXT(stored=True),
    platforms=TEXT(stored=True),
    position=ID(stored=True)
)

class Indexer:
    def __init__(self, configuration):
        self.configuration = configuration
        self.index_path = os.path.join(configuration.packages_index_folder, "index")
        if not os.path.exists(self.index_path):
            os.makedirs(self.index_path)
        self.storage = FileStorage(self.index_path)
        self.index = self.storage.create_index(schema)

    @staticmethod
    def bool_to_str(value):
        return value
        return "true" if value else "false"

    def index_packages(self, packages):
        writer = self.index.writer()
        for package in packages:
            writer.add_document(
                name=package.name,
                version=package.version,
                pname=package.pname,
                available=Indexer.bool_to_str(package.available),
                broken=Indexer.bool_to_str(package.broken),
                insecure=Indexer.bool_to_str(package.insecure),
                unfree=Indexer.bool_to_str(package.unfree),
                unsupported=Indexer.bool_to_str(package.unsupported),
                description=package.description,
                homepage=package.homepage,
                license_short_name=package.license_short_name,
                maintainers_name=",".join(package.maintainers_name),
                maintainers_github=",".join(package.maintainers_github),
                platforms=",".join(package.platforms),
                position=",".join(package.position)
            )
        writer.commit()
