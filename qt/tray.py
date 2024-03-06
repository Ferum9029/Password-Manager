from PyQt5 import QtWidgets, QtGui
from os import getcwd
# This file contains the tray setting


class TrayIcon(QtWidgets.QSystemTrayIcon):
    def __init__(self, window):
        super().__init__()
        # we get the window it's connected to
        self.window = window

        # da icon
        self.setIcon(QtGui.QIcon(getcwd()+'\\icons\\icon.ico'))

        # setting the possible options when the tray is RMBed
        show_action = QtWidgets.QAction("Show", self)
        quit_action = QtWidgets.QAction("Exit", self)

        show_action.triggered.connect(self.window.show)
        quit_action.triggered.connect(QtWidgets.QApplication.quit)

        tray_menu = QtWidgets.QMenu()
        tray_menu.addAction(show_action)
        tray_menu.addAction(quit_action)
        self.setContextMenu(tray_menu)
        self.show()

        # then doubleclick on the tray, the window shows up
        self.activated.connect(self.show_after_doubleclick)

    def show_after_doubleclick(self, reason):
        if reason == QtWidgets.QSystemTrayIcon.Trigger:
            self.window.show()
