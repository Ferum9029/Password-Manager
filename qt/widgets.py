from PyQt5 import QtWidgets, QtCore
import pyperclip


class TableWidget(QtWidgets.QTableWidget):
    def __init__(self, form):
        super().__init__(form)

        self.func_to_clear = None

        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setObjectName("tableWidget")
        self.setColumnCount(4)
        self.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.setHorizontalHeaderItem(3, item)
        self.horizontalHeader().setVisible(False)
        self.verticalHeader().setVisible(False)
        header = self.horizontalHeader()

        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(3, QtWidgets.QHeaderView.Stretch)

        self.itemDoubleClicked.connect(self._copy_item)

        self.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)

    def _copy_item(self, item: QtWidgets.QTableWidgetItem):
        pyperclip.copy(item.text())
        if item.column() == 3:
            QtCore.QTimer.singleShot(2500, lambda: self.clear() or self.func_to_clear())

    def add_row(self, data: tuple):
        rows_count = self.rowCount()
        self.setRowCount(rows_count+1)
        for i, item in enumerate(data):
            self.setItem(rows_count, i, TableWidgetItem(item))

    def clear(self):
        self.setRowCount(0)

    def set_func_to_clear(self, func):
        self.func_to_clear = func


class TableWidgetItem(QtWidgets.QTableWidgetItem):
    def __init__(self, *args):
        super().__init__(*args)
        self.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
