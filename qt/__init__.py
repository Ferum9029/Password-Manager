from PyQt5 import QtWidgets
import qt.main_window
import sys
from qt.error_handling import ErrorHandlers
from qt import errors

import qt.main_window


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = qt.main_window.MainWindow()
    try:
        window.show()
    except Exception as error:
        error_dial = errors.ErrorWindows()[error.__class__.__name__](error)
        error_dial.show()
        error_dial.exec_()
        ErrorHandlers[errors.ErrorCodes(error_dial.result()).name].value()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
