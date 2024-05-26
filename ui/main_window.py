import os

from PyQt5 import QtWidgets, QtCore, QtGui

from nixos.package import Package
from ui.package_window import PackageWindow


class NixGuiMainWindow(QtWidgets.QMainWindow):
    def __init__(self, configuration, parent=None):
        super().__init__(parent)
        self._packages = []
        self._package_windows = []
        self.configuration = configuration
        self.setWindowTitle('NixPkgs UI')

        # Central widget and layout
        central_widget = QtWidgets.QWidget()
        layout = QtWidgets.QGridLayout()

        # Full-size text input at the top
        self.text_input = self._get_search_input()
        self.text_input.returnPressed.connect(self.search)

        # Toggle boxes
        self.toggles = self._get_toggles()

        self.search_button = QtWidgets.QPushButton("Search")
        self.search_button.clicked.connect(self.search)

        self.package_view = self._get_package_view()

        layout.addWidget(self.text_input, 0, 0, 1, 999)
        layout.addWidget(self.search_button, 0, 998)
        for i, (key, value) in enumerate(self.toggles.items()):
            layout.addWidget(value, 1, i)
        layout.addWidget(self.package_view, 2, 0, 1, 999)

        layout.setSpacing(0)

        central_widget.setLayout(layout)

        self.setCentralWidget(central_widget)
        self.search()

    def _get_toggles(self):
        toggle_options = ["available", "working", "secure", "free", "good", "supported"]
        toggles = {}
        for option in toggle_options:
            toggles[option] = QtWidgets.QCheckBox(option)
            toggles[option].setTristate(True)
            toggles[option].setCheckState(QtCore.Qt.PartiallyChecked)
        return toggles

    def search(self):
        search_text = self.text_input.text()
        for key, value in self.toggles.items():
            if value.checkState() != QtCore.Qt.PartiallyChecked:
                search_text += f" {key}:" + ("t" if value.checkState() == QtCore.Qt.Checked else "f")
        print(f'Searching for: {search_text}')
        result = self.configuration.indexer.search(search_text)
        print(result)
        self._display_search_results(result)

    def _get_package_widget(self, res):
        widget = QtWidgets.QWidget()
        layout = QtWidgets.QGridLayout()
        icon_label = QtWidgets.QLabel()
        icon_label.setFixedWidth(75)
        icon_label.setFixedHeight(75)
        name_label = QtWidgets.QLabel(res['name'])
        name_label.setFont(QtGui.QFont("Arial", 12, QtGui.QFont.Bold))
        desc_label = QtWidgets.QLabel(res['description'])
        status_icons = self.get_status_boxes(res)
        layout.addWidget(icon_label, 0, 0, 2, 1)
        layout.addWidget(name_label, 0, 1)
        layout.addWidget(desc_label, 1, 1)
        layout.addWidget(status_icons, 0, 2, 2, 1)
        widget.setLayout(layout)

        return widget

    def get_status_boxes(self, res):
        widget = QtWidgets.QWidget()
        widget.setFixedWidth(100)
        widget.setFixedHeight(75)
        layout = QtWidgets.QGridLayout()
        toggle_options = ["available", "working", "secure", "free", "good", "supported"]
        icons = {}
        for option in toggle_options:
            icons[option] = QtWidgets.QCheckBox(option[0])
            icons[option].setCheckState(QtCore.Qt.Checked if res[option] else QtCore.Qt.Unchecked)
            icons[option].setDisabled(True)
            icons[option].setStyleSheet("QCheckBox::indicator { width: 20px; height: 20px; }")
            icons[option].setToolTip(option)

        for i, (key, value) in enumerate(icons.items()):
            layout.addWidget(value, i >= 3, 3 + (i % 3))
        widget.setLayout(layout)
        return widget

    def _display_search_results(self, result):
        self.package_view.clear()
        self.package_view.setColumnCount(1)
        self.package_view.setRowCount(len(result))
        for i, res in enumerate(result):
            self._packages.append(Package(self.configuration, res.fields()["key"]))
            package_widget = self._get_package_widget(res)
            self.package_view.setCellWidget(i, 0, package_widget)

    def _get_package_view(self):
        widget = QtWidgets.QTableWidget()
        widget.setColumnCount(1)
        widget.setHorizontalHeaderLabels(["Packages"])
        widget.horizontalHeader().setStretchLastSection(True)
        widget.verticalHeader().setVisible(False)
        widget.setShowGrid(False)
        widget.verticalHeader().setDefaultSectionSize(100)
        widget.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        widget.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        widget.cellDoubleClicked.connect(self.package_double_clicked)
        return widget

    def _get_search_input(self):
        text_input = QtWidgets.QLineEdit(self)
        text_input.setPlaceholderText("Enter text here")
        text_input.setText("minecraft")
        return text_input

    def package_double_clicked(self, row, column):
        package_window = PackageWindow(self._packages[row])
        package_window.show()
        self._package_windows.append(package_window)
