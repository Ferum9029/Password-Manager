from PyQt5 import QtWidgets, QtGui
from os import getcwd


class TrayIcon(QtWidgets.QSystemTrayIcon):
    def __init__(self, window):
        super().__init__()
        self.window = window

        self.setIcon(QtGui.QIcon(getcwd()+'\\icons\\icon.ico'))

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
