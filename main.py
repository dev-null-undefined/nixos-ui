import sys

from graphics.resource_manager import ResourceManager
from nixos.configuration import Configuration
from nixos.indexer import Indexer

from PyQt5 import QtWidgets

from ui.main_window import NixGuiMainWindow

resource_manager = ResourceManager()
conf = Configuration('nixos', 'nixpkgs', resource_manager)

indexer = Indexer(conf)
indexer.start(conf.packages)

conf.set_indexer(indexer)

# take user input
# search = input("Search: ")
# while search != "exit":
#     result = indexer.search(search)
#     print(result)
#     for r in result:
#         print(r)
#     search = input("Search: ")

app = QtWidgets.QApplication(sys.argv)
nix_gui = NixGuiMainWindow(conf)
nix_gui.show()
app.exec()