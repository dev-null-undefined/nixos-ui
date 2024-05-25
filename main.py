from nixos.configuration import Configuration

conf = Configuration('nixos')

print(conf.packages)

i = 0
for package in conf.packages:
    i += 1
    if i > 10:
        break
    print(package.attributes)