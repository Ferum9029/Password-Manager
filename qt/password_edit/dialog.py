from PyQt5 import QtWidgets
import generation
from qt.password_edit.parents import ControlLayout, ControlDialog


class AddPasswordLayout(ControlLayout):
    def __init__(self, parent=None):
        super().__init__(parent, "Add")

        self.spinBox = QtWidgets.QSpinBox()
        self.spinBox.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.spinBox.setValue(20)
        self.addWidget(self.spinBox, 1, 0, 1, 1)
        self.spinBox.valueChanged.connect(self._generate_and_show_password)

        self.password_lineEdit.setText(generation.generate(self.spinBox.value()))
        self.login_lineEdit.editingFinished.connect(self.password_lineEdit.selectAll)

    def _generate_and_show_password(self, count):
        self.password_lineEdit.setText(generation.generate(count))


class AddPasswordWindow(ControlDialog):
    def __init__(self, parent=None):
        super().__init__('Add password', parent)

        self.gridLayout = AddPasswordLayout(self)
        self.set_layout()


class EditPasswordLayout(ControlLayout):
    def __init__(self, source, info, login, password, parent=None):
        super().__init__(parent)

        self.source_lineEdit.setText(source)
        self.info_lineEdit.setText(info)
        self.login_lineEdit.setText(login)
        self.password_lineEdit.setText(password)

        self.GenerateButton = QtWidgets.QPushButton("Generate password")
        self.GenerateButton.setStyleSheet("background-color: None;")
        self.GenerateButton.setAutoDefault(False)
        self.GenerateButton.clicked.connect(self._generate_and_show_password)
        self.addWidget(self.GenerateButton, 1, 0, 1, 1)

        self.spinBox = QtWidgets.QSpinBox()
        self.spinBox.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.spinBox.setValue(20)
        self.addWidget(self.spinBox, 1, 1, 1, 1)

    def _generate_and_show_password(self):
        count = self.spinBox.value()
        self.password_lineEdit.setText(generation.generate(count))


class EditPasswordWindow(ControlDialog):
    def __init__(self, source, info, login, password, parent=None):
        super().__init__('Edit password', parent)

        self.gridLayout = EditPasswordLayout(source, info, login, password, self)
        self.set_layout()


class DeletePasswordLayout(ControlLayout):
    def __init__(self, password_data):
        super().__init__()

        self.source_lineEdit.setEnabled(False)
        self.info_lineEdit.setEnabled(False)
        self.login_lineEdit.setEnabled(False)
        self.password_lineEdit.setEnabled(False)

        self.source_lineEdit.setText(password_data[0])
        self.info_lineEdit.setText(password_data[1])
        self.login_lineEdit.setText(password_data[2])
        self.password_lineEdit.setText(password_data[3])

        self.DiscardButton.setAutoDefault(True)


class DeletePasswordWindow(ControlDialog):
    def __init__(self, password_data: tuple):
        super().__init__('Delete password?')

        self.gridLayout = DeletePasswordLayout(password_data)
        self.set_layout()
