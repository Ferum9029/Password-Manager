from PyQt5 import QtWidgets
import generation
from qt.dialogs.password_edit.parents import ControlLayout, ControlDialog
# Contains the password editing(adding, editing, deleting) windows


class AddPasswordLayout(ControlLayout):
    def __init__(self, parent=None):
        super().__init__(parent, "Add")

        # spingBox contains the number of symbols for password generation
        self.spinBox = QtWidgets.QSpinBox()
        self.spinBox.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        # 20 by default
        self.spinBox.setValue(20)
        self.addWidget(self.spinBox, 1, 0, 1, 1)
        # the number is changed - a new password is generated
        self.spinBox.valueChanged.connect(self._generate_and_show_password)

        # there is a randomly generated password in the password field
        self.password_lineEdit.setText(generation.generate(self.spinBox.value()))
        # because there's a random password in the field, we select it for easier editing
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

        # we need to see what we edit I guess -__-
        self.source_lineEdit.setText(source)
        self.info_lineEdit.setText(info)
        self.login_lineEdit.setText(login)
        self.password_lineEdit.setText(password)

        # the generate button there you have it
        self.GenerateButton = QtWidgets.QPushButton("Generate password")
        self.GenerateButton.setStyleSheet("background-color: None;")
        self.GenerateButton.setAutoDefault(False)
        self.GenerateButton.clicked.connect(self._generate_and_show_password)
        self.addWidget(self.GenerateButton, 1, 0, 1, 1)

        # spingBox contains the number of symbols for password generation
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

        # why would you edit a password you want to delete?
        # no reason to do it, so you can't do it
        self.source_lineEdit.setEnabled(False)
        self.info_lineEdit.setEnabled(False)
        self.login_lineEdit.setEnabled(False)
        self.password_lineEdit.setEnabled(False)

        # a user needs to see what they delete
        self.source_lineEdit.setText(password_data[0])
        self.info_lineEdit.setText(password_data[1])
        self.login_lineEdit.setText(password_data[2])
        self.password_lineEdit.setText(password_data[3])

        # I'd rather not delete than delete a password, so it's dumb(accident)-proof
        self.DiscardButton.setAutoDefault(True)


class DeletePasswordWindow(ControlDialog):
    def __init__(self, password_data: tuple):
        super().__init__('Delete password?')

        self.gridLayout = DeletePasswordLayout(password_data)
        self.set_layout()
