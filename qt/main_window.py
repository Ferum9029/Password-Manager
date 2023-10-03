from PyQt5 import QtWidgets, QtGui, QtCore
from os import getcwd
from qt.main_widget import MainMenu
from qt.tray import TrayIcon


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('PK')
        self.setWindowIcon(QtGui.QIcon(getcwd()+'\\icons\\logo.png'))
        self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint | QtCore.Qt.WindowMinimizeButtonHint)

        self.tray_icon = TrayIcon(self)
        self.tray_icon.setIcon(QtGui.QIcon(getcwd()+'\\icons\\logo.png'))

        self.setObjectName("QMainWindow")
        self.setMinimumSize(QtCore.QSize(421, 214))
        self.setStyleSheet('background-color: white;')

        self.SearchMenu = MainMenu()
        self.setCentralWidget(self.SearchMenu)

    def closeEvent(self, event):
        event.ignore()
        self.hide()
        self.tray_icon.show()
