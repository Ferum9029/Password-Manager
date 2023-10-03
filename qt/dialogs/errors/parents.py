from PyQt5 import QtWidgets, QtCore, QtGui


class ErrorLayout(QtWidgets.QGridLayout):
    def __init__(self, error_text, parent=None):
        super().__init__(parent)
        self.error = QtWidgets.QTextEdit()
        self.error.setText(error_text)
        self.error.setReadOnly(True)
        self.error.setStyleSheet('font-size: 16px;')
        self.error.setFrameStyle(QtWidgets.QFrame.NoFrame)
        self.addWidget(self.error, 0, 0, 1, 2)

        self.close_button = QtWidgets.QPushButton()
        self.close_button.setText('Close')
        self.close_button.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.close_button.setStyleSheet('background-color: None;')
        self.close_button.clicked.connect(self._reject)
        self.addWidget(self.close_button, 1, 1, 1, 1, alignment=QtCore.Qt.AlignRight)

    def _reject(self, *args):
        self.parent().reject()


class ErrorDialog(QtWidgets.QDialog):
    def __init__(self, error: Exception, parent=None, set_layout=True):
        super().__init__(parent=parent)
        error_text = f'{error.__class__.__name__}: {str(error)}'
        self.gridLayout = ErrorLayout(error_text)
        self.setWindowIcon(QtGui.QIcon('qt/icons/error_icon.png'))
        self.setWindowTitle('Error')
        self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint)
        self.setMinimumSize(QtCore.QSize(512, 128))
        self.setStyleSheet('background-color: white;')

        if set_layout:
            self.set_layout()

    def set_layout(self):
        self.setLayout(self.gridLayout)
