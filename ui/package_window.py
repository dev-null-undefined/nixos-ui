from random import randint

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QVBoxLayout, QLabel


class PackageWindow(QtWidgets.QWidget):

    def __init__(self, package, parent=None):
        super().__init__(parent)
        self.package = package
        self.setWindowTitle(f'NixPkgs UI - {package}')
        # self.setGeometry(100, 100, 800, 600)
        self.layout = QtWidgets.QGridLayout()
        self.package_name = QtWidgets.QLabel(str(package))
        self.layout.addWidget(self.package_name, 0, 0)
        self.setLayout(self.layout)