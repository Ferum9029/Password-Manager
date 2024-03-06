from PyQt5 import QtWidgets
import storage
import qt.dialogs.password_edit as password_edit
from qt.widgets import TableWidget
import storage.exceptions
import qt.dialogs.errors as errors
from qt.error_handling import ErrorHandlers


# The buttons with which you can add/edit/delete passwords
class PasswordEditLayout(QtWidgets.QGridLayout):
    def __init__(self, parent):
        super().__init__(parent)
        self.setObjectName('ButtonsGridLayout')

        # distance between the buttons themselves
        self.setContentsMargins(-1, 5, -1, -1)
        # The space between buttons and the upper window frame
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


# This is the layout of the table and the text fields above
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


# The main grid of the main menu
# It contains the grid layouts above
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

    # Function for easier button connection to their dedicated functions
    def connect_buttons(self, add, edit, delete):
        self.AddPassword.clicked.connect(add)
        self.EditPassword.clicked.connect(edit)
        self.DeletePassword.clicked.connect(delete)


# The menu itself
class MainMenu(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        # Setting the layout the contains all the needed buttons etc
        self.gridLayout = MainMenuGridLayout(self)
        self.setLayout(self.gridLayout)

        # Connecting buttons to the dedicated functions
        self.gridLayout.connect_buttons(self._add_password, self._edit_password, self._delete_password)

        # Connecting the event of editing text fields to the search function
        self.password_LineEdit = self.gridLayout.password_lineEdit
        self.password_LineEdit.textChanged.connect(self._search_password)

        self.login_LineEdit = self.gridLayout.login_lineEdit
        self.login_LineEdit.textChanged.connect(self._search_password)

        self.source_LineEdit = self.gridLayout.source_lineEdit
        self.source_LineEdit.textChanged.connect(self._search_password)

        # Setting the table and connecting the clear function
        self.password_Table = self.gridLayout.tableWidget
        self.password_Table.set_func_to_clear(self.clear_lineEdits)

        self.setContentsMargins(0, 0, 0, 0)

        # Setting and connecting the DB, if there's been an error, calling the Error Window
        try:
            self.storage = storage.DB()
        except Exception as e:
            self._handle_error(e)
            self.storage = storage.DB()
        self.storage.connect()

    def _handle_error(self, error):
        # Choosing the appropriate error window \/ and initializing it \/
        error_dial = errors.ErrorWindows()[error.__class__.__name__](error)
        error_dial.show()
        error_dial.exec_()
        # From the error dialogue we fetch the error code (from .result() method)
        # From ErrorCodes we get the name of the needed method using the fetched error code
        # Using the found name we get the needed function from ErrorHandlers, value method is to get the func itself
        # call the found function
        ErrorHandlers[errors.ErrorCodes(error_dial.result()).name].value()

    # The func clears search fields (called if a password's been copied)
    def clear_lineEdits(self):
        self.password_LineEdit.clear()
        self.login_LineEdit.clear()
        self.source_LineEdit.clear()

    def _add_row_to_table(self, data: tuple):
        self.password_Table.add_row(data)

    def _clear_table(self):
        self.password_Table.clear()

    def _search_password(self, _):
        # remove already found password from the table
        self._clear_table()
        source, login = self.source_LineEdit.text(), self.login_LineEdit.text()
        password = self.password_LineEdit.text()
        # if all fields are empty - no passwords to look up
        if not any((source, login, password)):
            return
        try:
            matched_passwords = self.storage.get_matched_passwords(source=source, login=login, password=password)
        except Exception as e:
            # just in case there's been an error (shouldn't happen)
            self._handle_error(e)
            matched_passwords = self.storage.get_matched_passwords(source=source, login=login, password=password)

        # showing the found passwords
        for pw_data in matched_passwords:
            self._add_row_to_table(pw_data)

    def _add_password(self):
        # starting the add password window
        add_password_dialog = password_edit.AddPasswordWindow()
        add_password_dialog.show()
        add_password_dialog.exec_()
        # if the password is not discarded, adding it
        if add_password_dialog.result():
            source, info, login, password = add_password_dialog.get_values()
            self.storage.add_password(source, info, login, password)

    def _edit_password(self):
        # finding the number of the row the password at
        row = self.password_Table.currentRow()
        if row == -1:
            return

        # gathering the password-to-edit info
        source, info = self.password_Table.item(row, 0).text(), self.password_Table.item(row, 1).text()
        login, password = self.password_Table.item(row, 2).text(), self.password_Table.item(row, 3).text()

        # starting the editing window
        edit_password_dialog = password_edit.EditPasswordWindow(source, info, login, password)
        edit_password_dialog.show()
        edit_password_dialog.exec_()
        old_password_data = (source, info, login, password,)
        if edit_password_dialog.result():
            new_password_data = tuple(edit_password_dialog.get_values())
            # editing the password
            self.storage.edit_password(old_password_data, new_password_data)
            self._clear_table()
            self.clear_lineEdits()

    def _delete_password(self):
        # finding the number of the row the password at
        row = self.password_Table.currentRow()
        if row == -1:
            return

        # gathering the password-to-edit info
        source, info = self.password_Table.item(row, 0).text(), self.password_Table.item(row, 1).text()
        login, password = self.password_Table.item(row, 2).text(), self.password_Table.item(row, 3).text()

        # starting the deletion window
        delete_password_dialog = password_edit.DeletePasswordWindow((source, info, login, password,))
        delete_password_dialog.show()
        delete_password_dialog.exec_()
        # deleting the password if the user is sure
        if delete_password_dialog.result():
            source, info, login, password = delete_password_dialog.get_values()
            self.storage.delete_password(source, info, login, password)
            # updating the password table
            self._search_password('')
