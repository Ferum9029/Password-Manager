from PyQt5 import QtWidgets, QtCore, QtGui


class ControlLayout(QtWidgets.QGridLayout):
    def __init__(self, parent=None, accept_button_name='Accept'):
        super().__init__(parent)

        self.setContentsMargins(-1, 10, -1, -1)
        self.setVerticalSpacing(2)

        self.source_lineEdit = QtWidgets.QLineEdit()
        self.source_lineEdit.setPlaceholderText("Source")
        self.addWidget(self.source_lineEdit, 0, 0, 1, 1)

        self.info_lineEdit = QtWidgets.QLineEdit()
        self.info_lineEdit.setPlaceholderText("Info")
        self.addWidget(self.info_lineEdit, 0, 1, 1, 1)

        self.login_lineEdit = QtWidgets.QLineEdit()
        self.login_lineEdit.setPlaceholderText("Login")
        self.addWidget(self.login_lineEdit, 0, 2, 1, 1)

        self.password_lineEdit = QtWidgets.QLineEdit()
        self.password_lineEdit.setPlaceholderText("Password")
        self.addWidget(self.password_lineEdit, 0, 3, 1, 1)

        self.DiscardButton = QtWidgets.QPushButton('Discard')
        self.DiscardButton.setStyleSheet('background-color: None;')
        self.DiscardButton.setAutoDefault(False)
        self.DiscardButton.clicked.connect(self._close_parent)
        self.addWidget(self.DiscardButton, 1, 3, 1, 1)

        self.AcceptButton = QtWidgets.QPushButton(accept_button_name)
        self.AcceptButton.setStyleSheet('background-color: None;')
        self.AcceptButton.setAutoDefault(False)
        self.AcceptButton.clicked.connect(self._accept)
        self.addWidget(self.AcceptButton, 1, 2, 1, 1)

        self.source_lineEdit.returnPressed.connect(self.info_lineEdit.setFocus)
        self.info_lineEdit.returnPressed.connect(self.login_lineEdit.setFocus)
        self.login_lineEdit.returnPressed.connect(self.password_lineEdit.setFocus)
        self.password_lineEdit.returnPressed.connect(self.password_lineEdit.clearFocus)
        self.password_lineEdit.returnPressed.connect(self._set_add_button_focused)

    def _close_parent(self, *args):
        self.parent().reject()

    def _accept(self, *args):
        self.parent().accept()

    def _set_add_button_focused(self):
        QtCore.QTimer.singleShot(0, lambda: self.AcceptButton.setDefault(True))

    def get_values(self):
        source = self.source_lineEdit.text()
        info = self.info_lineEdit.text()
        login = self.login_lineEdit.text()
        password = self.password_lineEdit.text()
        return source, info, login, password


class ControlDialog(QtWidgets.QDialog):
    def __init__(self, name, parent=None):
        super().__init__(parent=parent)
        self.setWindowTitle(name)
        self.setWindowIcon(QtGui.QIcon('qt/icons/logo.png'))
        self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint)
        self.setMinimumSize(QtCore.QSize(280, 70))
        self.setStyleSheet('background-color: white;')

        self.gridLayout = ControlLayout()

    def set_layout(self):
        self.setLayout(self.gridLayout)

    def get_values(self):
        return self.gridLayout.get_values()
