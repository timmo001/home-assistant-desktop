"""Home Assistant Desktop: GUI - Settings"""
import random

from PySide6 import QtCore, QtWidgets


class GUISettings(QtWidgets.QWidget):
    """GUI - Settings"""

    def __init__(self):
        """Initialize"""
        super().__init__()

        self.hello = ["Hallo Welt", "Hei maailma", "Hola Mundo"]

        self.button = QtWidgets.QPushButton("Click me!")
        self.text = QtWidgets.QLabel(
            "Hello World",
            alignment=QtCore.Qt.AlignCenter,
        )  # type: ignore

        self.layout = QtWidgets.QVBoxLayout(self)  # type: ignore
        self.layout.addWidget(self.text)
        self.layout.addWidget(self.button)

        self.button.clicked.connect(self.magic)  # type: ignore

    @QtCore.Slot()
    def magic(self):
        """Magic"""
        self.text.setText(random.choice(self.hello))
