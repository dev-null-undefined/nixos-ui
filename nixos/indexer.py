"""
TODO
"""
import os

from whoosh.fields import Schema, TEXT, ID, BOOLEAN, NGRAM, KEYWORD
from whoosh.filedb.filestore import FileStorage
from whoosh.index import EmptyIndexError
from whoosh.qparser import MultifieldParser, FieldAliasPlugin

schema = Schema(
    name=TEXT(stored=True),
    key=ID(stored=True),
    version=TEXT(stored=True),
    pname=TEXT(stored=True),
    available=BOOLEAN(stored=True),
    working=BOOLEAN(stored=True),
    secure=BOOLEAN(stored=True),
    free=BOOLEAN(stored=True),
    good=BOOLEAN(stored=True),
    supported=BOOLEAN(stored=True),
    description=TEXT(stored=True),
    homepage=ID(stored=True),
    license_short_name=TEXT(stored=True),
    maintainers_name=NGRAM(stored=True),
    maintainers_github=TEXT(stored=True),
    platforms=KEYWORD(stored=True, commas=True),
    position=ID(stored=True)
)


class Indexer:
    """
    Indexer for searching for packages
    """

    def __init__(self, configuration):
        self.configuration = configuration
        self.index_path = os.path.join(configuration.packages_index_folder, "index")
        if not os.path.exists(self.index_path):
            os.makedirs(self.index_path)
        self.storage = FileStorage(self.index_path)
        self.index = None
        self.searcher = None

    def start(self, packages):
        """
        Start the indexer try to load the index from the storage, if it is empty or not present, create a new index
        Or if the index has fewer elements than we have packages, reindex the packages
        :param packages:
        :return:
        """
        try:
            self.index = self.storage.open_index()
        except EmptyIndexError:
            self.index = None
        if not self.index or self.index.is_empty() or self.index.doc_count() < len(packages):
            self.index = self.storage.create_index(schema)
            self._index_packages(packages)
        self.searcher = self.index.searcher()

    def _index_packages(self, packages):
        writer = self.index.writer()
        counter = 0
        for package in packages:
            counter += 1
            if counter % (len(packages) // 20) == 0:
                print(f"Indexing {counter}/{len(packages)}")
            writer.add_document(
                name=package.name,
                key=package.key,
                version=package.version,
                pname=package.pname,
                available=package.available,
                good=package.good,
                working=package.working,
                secure=package.secure,
                free=package.free,
                supported=package.supported,
                description=package.description,
                homepage=package.homepage,
                license_short_name=package.license_short_name,
                maintainers_name=",".join(package.maintainers_name),
                maintainers_github=",".join(package.maintainers_github),
                platforms=",".join(package.platforms),
                position=package.position
            )
        writer.commit()

    def search(self, query, limit=100):
        """
        Search the index for packages matching the query
        :param query:
        :param limit:
        :return:
        """
        query_parser = MultifieldParser(["name", "description"], schema=self.index.schema)
        query_parser.add_plugin(FieldAliasPlugin({"description": ["desc", "text", "info", "props", "properties", "use"],
                                                  "name": ["title"]}))
        query = query_parser.parse(query)
        for subquery in query.all_terms():
            if subquery[0] == "name" and subquery[1] == "free":
                query.subqueries.append(query_parser.parse("free:true"))

        results = self.searcher.search(query, limit=limit)

        return results
