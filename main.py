from nixos.configuration import Configuration
from nixos.indexer import Indexer

conf = Configuration('nixos')

print(conf.packages)

i = 0
for package in conf.packages:
    i += 1
    if i > 10:
        break
    print(
                package.name,
                package.version,
                package.pname,
                package.available,
                package.broken,
                package.insecure,
                package.unfree,
                package.unsupported,
                package.description,
                package.homepage,
                package.license_short_name,
                package.maintainers_name,
                package.maintainers_github,
                package.platforms,
                package.position)

indexer = Indexer(conf)

indexer.index_packages(conf.packages)