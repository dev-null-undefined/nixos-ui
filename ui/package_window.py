"""
Package window
"""
import subprocess

from PyQt5 import QtWidgets


class PackageWindow(QtWidgets.QWidget):
    """
    Create package window for displaying package information
    """

    def __init__(self, package, parent=None):
        """
        Initialize package window
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
        build_button = QtWidgets.QPushButton('Build')
        build_button.clicked.connect(self._build)
        self.layout.addWidget(build_button, 0, 1)
        self.setLayout(self.layout)

    def _build(self):
        print(f'Building {self.package.key}-{self.package.version}')
        package_path = self.package.build()
        subprocess.run(['xdg-open', package_path], check=False)


