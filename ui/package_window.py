"""
TODO
"""
from PyQt5 import QtWidgets


class PackageWindow(QtWidgets.QWidget):
    """
    TODO
    """

    def __init__(self, package, parent=None):
        """
        TODO
        :param package:
        :param parent:
        """
        super().__init__(parent)
        self.package = package
        self.setWindowTitle(f'NixPkgs UI - {package.key}-{package.version}')
        # self.setGeometry(100, 100, 800, 600)
        self.layout = QtWidgets.QGridLayout()
        self.package_name = QtWidgets.QLabel(str(package))
        self.layout.addWidget(self.package_name, 0, 0)
        self.setLayout(self.layout)
