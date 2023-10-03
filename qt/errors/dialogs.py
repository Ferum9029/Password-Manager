from PyQt5 import QtWidgets, QtCore
from qt.errors.parents import ErrorDialog, ErrorLayout
from qt.errors.error_codes import ErrorCodes


class KeyFileNotFoundLayout(ErrorLayout):
    def __init__(self, error_text):
        super(KeyFileNotFoundLayout, self).__init__(error_text)

        self.error.setText(self.error.toPlainText() +
                           '\n\nIf you press "Close" nothing will be done and app will be closed'
                           '\nIf you press "Delete database", your passwords will be erased, but the error will be done')

        self.delete_button = QtWidgets.QPushButton()
        self.delete_button.setText('Delete database')
        self.delete_button.setStyleSheet('background-color: None;')
        self.delete_button.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.delete_button.clicked.connect(self._accept)

        self.addWidget(self.delete_button, 1, 0, 1, 1, alignment=QtCore.Qt.AlignLeft)

    def _accept(self, *args):
        self.parent().done(ErrorCodes.DELETE_DATABASE.value)


class KeyFileNotFoundDialog(ErrorDialog):
    def __init__(self, error, parent=None):
        error_text = f'{error.__class__.__name__}: {str(error)}'
        super().__init__(error, parent=parent, set_layout=False)

        self.gridLayout = KeyFileNotFoundLayout(error_text)
        self.set_layout()


class KeyDoesntFitLayout(ErrorLayout):
    def __init__(self, error_text):
        super().__init__(error_text)

        self.error.setText(self.error.toPlainText() +
                           '\n\nIf you press "Close" nothing will be done and app will be closed'
                           '\nIf you press "Delete database", your passwords will be erased, but the error will be done')

        self.delete_button = QtWidgets.QPushButton()
        self.delete_button.setText('Delete database')
        self.delete_button.setStyleSheet('background-color: None;')
        self.delete_button.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.delete_button.clicked.connect(self._accept)

        self.addWidget(self.delete_button, 1, 0, 1, 1, alignment=QtCore.Qt.AlignLeft)

    def _accept(self, *args):
        self.parent().done(ErrorCodes.DELETE_DATABASE.value)


class KeyDoesntFitDialog(ErrorDialog):
    def __init__(self, error, parent=None):
        error_text = f'{error.__class__.__name__}: {str(error)}'
        super().__init__(error, parent=parent, set_layout=False)

        self.gridLayout = KeyFileNotFoundLayout(error_text)
        self.set_layout()
