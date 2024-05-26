import os
from threading import Thread

from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import Qt

from nixos.package import Package
from ui.package_window import PackageWindow

MAX_ICON_LOAD_AT_ONCE = 10


class IconLoaderThread(QtCore.QThread):
    data_downloaded = QtCore.pyqtSignal(object)

    def __init__(self, main_window):
        QtCore.QThread.__init__(self)
        self.main_window = main_window

    def run(self):
        self._load_icon()

    def _load_icon(self):
        while len(self.main_window._icon_queue) != 0:
            homepage = self.main_window._icon_queue[0]
            self.main_window._icon_queue = self.main_window._icon_queue[1:]
            if not homepage or homepage == "null" or homepage == "None" or homepage == "":
                continue
            print("Loading icon for: ", homepage)
            icon = self.main_window.configuration.resource_manager.get_favicon(homepage)
            if icon is not None:
                print("Icon loaded for: ", homepage, ", ", icon.path)
            self.data_downloaded.emit(homepage)
            if len(self.main_window._icon_queue) == 0:
                self.main_window._icon_loading_queue -= 1
                return


class NixGuiMainWindow(QtWidgets.QMainWindow):
    def __init__(self, configuration, parent=None):
        super().__init__(parent)
        self._packages = []
        self._pixmaps = []
        self._icon_queue = []
        self._icon_labels = {}
        self._threads = []
        self._icon_loading_queue = 0
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
        if res['homepage'] not in self._icon_labels:
            self._icon_labels[res['homepage']] = [icon_label]
            self._icon_queue.append(res['homepage'])
        else:
            self._icon_labels[res['homepage']].append(icon_label)
        return widget

    def get_status_boxes(self, res):
        widget = QtWidgets.QWidget()
        widget.setFixedWidth(100)
        widget.setFixedHeight(75)
        layout = QtWidgets.QGridLayout()
        toggle_options = ["available", "working", "secure", "free", "good", "supported"]
        toggle_checkboxes = {}
        for option in toggle_options:
            toggle_checkboxes[option] = QtWidgets.QCheckBox(option[0])
            toggle_checkboxes[option].setCheckState(QtCore.Qt.Checked if res[option] else QtCore.Qt.Unchecked)
            toggle_checkboxes[option].setDisabled(True)
            toggle_checkboxes[option].setStyleSheet("QCheckBox::indicator { width: 20px; height: 20px; }")
            toggle_checkboxes[option].setToolTip(option)

        for i, (key, value) in enumerate(toggle_checkboxes.items()):
            layout.addWidget(value, i >= 3, 3 + (i % 3))
        widget.setLayout(layout)
        return widget

    def _display_search_results(self, result):
        self.package_view.clear()
        self.package_view.setColumnCount(1)
        self.package_view.setRowCount(len(result))
        self._packages = []
        self._icon_queue = []
        self._icon_labels = {}
        for i, res in enumerate(result):
            self._packages.append(Package(self.configuration, res.fields()["key"]))
            package_widget = self._get_package_widget(res)
            self.package_view.setCellWidget(i, 0, package_widget)
        self._start_icon_queue()

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

    def _start_icon_queue(self):
        while self._icon_loading_queue < MAX_ICON_LOAD_AT_ONCE:
            thread = IconLoaderThread(self)
            thread.data_downloaded.connect(self._on_icon_read)
            thread.start()
            self._threads.append(thread)
            # thread.join()
            self._icon_loading_queue += 1

    def _on_icon_read(self, url):
        print("Icon loaded for: ", url)
        for icon_label in self._icon_labels[url]:
            icon = self.configuration.resource_manager.get_favicon(url)
            if icon is None:
                continue
            pixmap = QtGui.QPixmap(icon.path)
            assert os.path.exists(icon.path)
            self._pixmaps.append(pixmap)
            icon_label.setPixmap(pixmap)
            icon_label.setScaledContents(True)
        del self._icon_labels[url]
