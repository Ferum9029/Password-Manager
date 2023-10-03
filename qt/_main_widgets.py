import os
import sys

from PyQt5 import QtWidgets, QtCore, QtGui
import storage
from . import dialogs
from qt.widgets import TableWidget
import storage.exceptions


class TrayIcon(QtWidgets.QSystemTrayIcon):
    def __init__(self, window):
        super().__init__()
        self.window = window

        self.setIcon(QtGui.QIcon('./icons/icon.ico'))

        show_action = QtWidgets.QAction("Show", self)
        quit_action = QtWidgets.QAction("Exit", self)

        show_action.triggered.connect(self.window.show)
        quit_action.triggered.connect(QtWidgets.QApplication.quit)

        tray_menu = QtWidgets.QMenu()
        tray_menu.addAction(show_action)
        tray_menu.addAction(quit_action)
        self.setContextMenu(tray_menu)
        self.show()

        self.activated.connect(self.show_after_doubleclick)

    def show_after_doubleclick(self, reason):
        if reason == QtWidgets.QSystemTrayIcon.Trigger:
            self.window.show()


class PasswordEditLayout(QtWidgets.QGridLayout):
    def __init__(self, parent):
        super().__init__(parent)
        self.setObjectName('ButtonsGridLayout')

        self.setContentsMargins(-1, 5, -1, -1)
        self.setVerticalSpacing(2)

        self.AddPassword = QtWidgets.QPushButton('Add Password')
        self.AddPassword.setStyleSheet('background-color: None')
        self.addWidget(self.AddPassword, 0, 0, 1, 1)

        self.EditPassword = QtWidgets.QPushButton('Edit Password')
        self.EditPassword.setStyleSheet('background-color: None')
        self.addWidget(self.EditPassword, 0, 1, 1, 1)

        self.DeletePassword = QtWidgets.QPushButton('Delete Password')
        self.DeletePassword.setStyleSheet('background-color: None')
        self.addWidget(self.DeletePassword, 0, 2, 1, 1)


class PasswordTableLayout(QtWidgets.QGridLayout):
    def __init__(self, parent, info_enabled=False):
        super().__init__(parent)
        self.setObjectName('SearcherGridLayout')

        self.setContentsMargins(-1, 5, -1, -1)
        self.setVerticalSpacing(2)

        self.password_lineEdit = QtWidgets.QLineEdit()
        self.password_lineEdit.setPlaceholderText("Password")
        self.addWidget(self.password_lineEdit, 1, 3, 1, 1)

        self.source_lineEdit = QtWidgets.QLineEdit()
        self.source_lineEdit.setPlaceholderText("Source")
        self.addWidget(self.source_lineEdit, 1, 0, 1, 1)

        self.info_lineEdit = QtWidgets.QLineEdit()
        self.info_lineEdit.setPlaceholderText("Info")
        self.info_lineEdit.setEnabled(info_enabled)
        self.addWidget(self.info_lineEdit, 1, 1, 1, 1)

        self.login_lineEdit = QtWidgets.QLineEdit()
        self.login_lineEdit.setPlaceholderText("Login")
        self.addWidget(self.login_lineEdit, 1, 2, 1, 1)

        self.tableWidget = TableWidget(parent)
        self.addWidget(self.tableWidget, 2, 0, 1, 4)


class MainMenuGridLayout(QtWidgets.QGridLayout):
    def __init__(self, parent):
        super(MainMenuGridLayout, self).__init__(parent)
        self.setObjectName('gridLayout')

        self.ButtonsGrid = PasswordEditLayout(parent)
        self.addLayout(self.ButtonsGrid, 0, 0, 1, 1)

        self.AddPassword = self.ButtonsGrid.AddPassword
        self.EditPassword = self.ButtonsGrid.EditPassword
        self.DeletePassword = self.ButtonsGrid.DeletePassword

        self.SearchGrid = PasswordTableLayout(parent)
        self.addLayout(self.SearchGrid, 1, 0, 1, 1)

        self.password_lineEdit = self.SearchGrid.password_lineEdit
        self.login_lineEdit = self.SearchGrid.login_lineEdit
        self.source_lineEdit = self.SearchGrid.source_lineEdit
        self.tableWidget = self.SearchGrid.tableWidget

        self.setContentsMargins(2, 0, 2, 2)
        self.setVerticalSpacing(0)

    def connect_buttons(self, add, edit, delete):
        self.AddPassword.clicked.connect(add)
        self.EditPassword.clicked.connect(edit)
        self.DeletePassword.clicked.connect(delete)


class MainMenu(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.gridLayout = MainMenuGridLayout(self)
        self.setLayout(self.gridLayout)

        self.gridLayout.connect_buttons(self._add_password, self._edit_password, self._delete_password)

        self.password_LineEdit = self.gridLayout.password_lineEdit
        self.password_LineEdit.textChanged.connect(self._search_password)

        self.login_LineEdit = self.gridLayout.login_lineEdit
        self.login_LineEdit.textChanged.connect(self._search_password)

        self.source_LineEdit = self.gridLayout.source_lineEdit
        self.source_LineEdit.textChanged.connect(self._search_password)

        self.password_Table = self.gridLayout.tableWidget
        self.password_Table.set_func_to_clear(self.clear_lineEdits)

        self.setContentsMargins(0, 0, 0, 0)

        try:
            self.storage = storage.DB()
        except storage.exceptions.KeyFileNotFound as e:
            self._show_key_error(e)
        else:
            self.storage.connect()

    def _show_key_error(self, error):
        error_dial = dialogs.ErrorWindows()[error.__class__.__name__](error)
        error_dial.show()
        error_dial.exec_()
        if not error_dial.result():
            sys.exit()
        storage.delete_db()
        self.storage = storage.DB()
        self.storage.connect()

    def clear_lineEdits(self):
        self.password_LineEdit.clear()
        self.login_LineEdit.clear()
        self.source_LineEdit.clear()

    def _add_row_to_table(self, data: tuple):
        self.password_Table.add_row(data)

    def _clear_table(self):
        self.password_Table.clear()

    def _search_password(self, _):
        self._clear_table()
        source, login = self.source_LineEdit.text(), self.login_LineEdit.text()
        password = self.password_LineEdit.text()
        if not any((source, login, password)):
            return
        matched_passwords = self.storage.get_matched_passwords(source=source, login=login, password=password)
        for pw_data in matched_passwords:
            self._add_row_to_table(pw_data)

    def _add_password(self):
        add_password_dialog = dialogs.AddPasswordWindow()
        add_password_dialog.show()
        add_password_dialog.exec_()
        if add_password_dialog.result():
            source, info, login, password = add_password_dialog.get_values()
            self.storage.add_password(source, info, login, password)

    def _edit_password(self):
        row = self.password_Table.currentRow()
        if row == -1:
            return

        source, info = self.password_Table.item(row, 0).text(), self.password_Table.item(row, 1).text()
        login, password = self.password_Table.item(row, 2).text(), self.password_Table.item(row, 3).text()

        edit_password_dialog = dialogs.EditPasswordWindow(source, info, login, password)
        edit_password_dialog.show()
        edit_password_dialog.exec_()
        old_password_data = (source, info, login, password,)
        if edit_password_dialog.result():
            new_password_data = tuple(edit_password_dialog.get_values())
            self.storage.edit_password(old_password_data, new_password_data)
            self._clear_table()
            self.clear_lineEdits()

    def _delete_password(self):
        row = self.password_Table.currentRow()
        if row == -1:
            return

        source, info = self.password_Table.item(row, 0).text(), self.password_Table.item(row, 1).text()
        login, password = self.password_Table.item(row, 2).text(), self.password_Table.item(row, 3).text()

        delete_password_dialog = dialogs.DeletePasswordWindow((source, info, login, password,))
        delete_password_dialog.show()
        delete_password_dialog.exec_()
        if delete_password_dialog.result():
            source, info, login, password = delete_password_dialog.get_values()
            self.storage.delete_password(source, info, login, password)
            self._search_password('')


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('PK')
        self.setWindowIcon(QtGui.QIcon('qt/icons/logo.png'))
        self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint | QtCore.Qt.WindowMinimizeButtonHint)

        self.tray_icon = TrayIcon(self)
        self.tray_icon.setIcon(QtGui.QIcon('qt/icons/logo.png'))

        self.setObjectName("QMainWindow")
        self.setMinimumSize(QtCore.QSize(421, 214))
        self.setStyleSheet('background-color: white;')

        self.SearchMenu = MainMenu()
        self.setCentralWidget(self.SearchMenu)

    def closeEvent(self, event):
        event.ignore()
        self.hide()
        self.tray_icon.show()
