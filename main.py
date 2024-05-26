from nixos.configuration import Configuration
from nixos.indexer import Indexer

conf = Configuration('nixos', 'nixpkgs-master')

indexer = Indexer(conf)
indexer.start(conf.packages)

result = indexer.search("free")
# take user input
search = input("Search: ")
while search != "exit":
    result = indexer.search(search)
    print(result)
    for r in result:
        print(r)
    search = input("Search: ")