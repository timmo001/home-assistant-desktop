"""Home Assistant Desktop: GUI - Settings"""
from collections.abc import Callable

from PySide6 import QtCore, QtGui, QtWidgets

from ..const import (
    SECRET_HOME_ASSISTANT_TOKEN,
    SETTING_AUTOSTART,
    SETTING_HOME_ASSISTANT_HOST,
    SETTING_HOME_ASSISTANT_PORT,
    SETTING_HOME_ASSISTANT_SECURE,
    SETTING_LOG_LEVEL,
)
from ..settings import Settings


class GUISettings(QtWidgets.QWidget):
    """GUI - Settings"""

    def __init__(
        self,
        callback: Callable[[str], None],
        settings: Settings,
    ):
        """Initialize"""
        super().__init__()

        self._callback = callback
        self._settings = settings

        setting_autostart: bool = bool(self._settings.get(SETTING_AUTOSTART))
        setting_log_level: str = str(self._settings.get(SETTING_LOG_LEVEL))
        setting_home_assistant_secure: bool = bool(
            self._settings.get(SETTING_HOME_ASSISTANT_SECURE)
        )
        setting_home_assistant_host: str = str(
            self._settings.get(SETTING_HOME_ASSISTANT_HOST)
        )
        setting_home_assistant_port: str = str(
            self._settings.get(SETTING_HOME_ASSISTANT_PORT)
        )
        secret_home_assistant_token: str = str(
            self._settings.get_secret(SECRET_HOME_ASSISTANT_TOKEN)
        )

        label_heading = QtWidgets.QLabel("Settings")
        label_heading.setFont(QtGui.QFont("Roboto", 38, QtGui.QFont.Light))

        label_general = QtWidgets.QLabel("General")
        label_general.setFont(QtGui.QFont("Roboto", 24, QtGui.QFont.Light))

        label_autostart = QtWidgets.QLabel("Autostart")
        label_autostart.setFont(QtGui.QFont("Roboto", 10))
        self.input_autostart = QtWidgets.QCheckBox()
        self.input_autostart.setCheckState(
            QtCore.Qt.CheckState.Checked
            if setting_autostart
            else QtCore.Qt.CheckState.Unchecked
        )
        layout_autostart = QtWidgets.QHBoxLayout()
        layout_autostart.setSpacing(8)
        layout_autostart.setContentsMargins(8, 0, 8, 0)
        layout_autostart.addWidget(label_autostart, stretch=0)
        layout_autostart.addWidget(
            self.input_autostart, stretch=1, alignment=QtCore.Qt.AlignRight
        )

        label_log_level = QtWidgets.QLabel("Log Level")
        label_log_level.setFont(QtGui.QFont("Roboto", 10))
        self.input_log_level = QtWidgets.QLineEdit()
        self.input_log_level.setPlaceholderText("INFO")
        self.input_log_level.setText(setting_log_level)
        layout_log_level = QtWidgets.QHBoxLayout()
        layout_log_level.setSpacing(8)
        layout_log_level.setContentsMargins(8, 0, 8, 0)
        layout_log_level.addWidget(label_log_level, stretch=0)
        layout_log_level.addWidget(
            self.input_log_level, stretch=1, alignment=QtCore.Qt.AlignRight
        )

        label_home_assistant = QtWidgets.QLabel("Home Assistant")
        label_home_assistant.setFont(QtGui.QFont("Roboto", 24, QtGui.QFont.Light))

        label_home_assistant_host = QtWidgets.QLabel("Host")
        label_home_assistant_host.setFont(QtGui.QFont("Roboto", 10))
        self.input_home_assistant_host = QtWidgets.QLineEdit()
        self.input_home_assistant_host.setPlaceholderText("homeassistant.local")
        self.input_home_assistant_host.setText(setting_home_assistant_host)
        layout_home_assistant_host = QtWidgets.QHBoxLayout()
        layout_home_assistant_host.setSpacing(8)
        layout_home_assistant_host.setContentsMargins(8, 0, 8, 0)
        layout_home_assistant_host.addWidget(label_home_assistant_host, stretch=0)
        layout_home_assistant_host.addWidget(
            self.input_home_assistant_host, stretch=1, alignment=QtCore.Qt.AlignRight
        )

        label_home_assistant_port = QtWidgets.QLabel("Port")
        label_home_assistant_port.setFont(QtGui.QFont("Roboto", 10))
        self.input_home_assistant_port = QtWidgets.QLineEdit()
        self.input_home_assistant_port.setPlaceholderText("8123")
        self.input_home_assistant_port.setText(setting_home_assistant_port)
        layout_home_assistant_port = QtWidgets.QHBoxLayout()
        layout_home_assistant_port.setSpacing(8)
        layout_home_assistant_port.setContentsMargins(8, 0, 8, 0)
        layout_home_assistant_port.addWidget(label_home_assistant_port, stretch=0)
        layout_home_assistant_port.addWidget(
            self.input_home_assistant_port, stretch=1, alignment=QtCore.Qt.AlignRight
        )

        label_home_assistant_secure = QtWidgets.QLabel("SSL")
        label_home_assistant_secure.setFont(QtGui.QFont("Roboto", 10))
        self.input_home_assistant_secure = QtWidgets.QCheckBox()
        self.input_home_assistant_secure.setCheckState(
            QtCore.Qt.CheckState.Checked
            if setting_home_assistant_secure
            else QtCore.Qt.CheckState.Unchecked
        )
        layout_home_assistant_secure = QtWidgets.QHBoxLayout()
        layout_home_assistant_secure.setSpacing(8)
        layout_home_assistant_secure.setContentsMargins(8, 0, 8, 0)
        layout_home_assistant_secure.addWidget(label_home_assistant_secure, stretch=0)
        layout_home_assistant_secure.addWidget(
            self.input_home_assistant_secure, stretch=1, alignment=QtCore.Qt.AlignRight
        )

        label_home_assistant_token = QtWidgets.QLabel("Token")
        label_home_assistant_token.setFont(QtGui.QFont("Roboto", 10))
        self.input_home_assistant_token = QtWidgets.QLineEdit()
        self.input_home_assistant_token.setText(secret_home_assistant_token)
        # self.input_home_assistant_token.setEchoMode(
        #     QtWidgets.QLineEdit.EchoMode.Password
        # )
        # self.input_home_assistant_token.setPlaceholderText("********")
        layout_home_assistant_token = QtWidgets.QHBoxLayout()
        layout_home_assistant_token.setSpacing(8)
        layout_home_assistant_token.setContentsMargins(8, 0, 8, 0)
        layout_home_assistant_token.addWidget(label_home_assistant_token, stretch=1)
        layout_home_assistant_token.addWidget(
            self.input_home_assistant_token, stretch=2, alignment=QtCore.Qt.AlignRight
        )

        layout_general = QtWidgets.QVBoxLayout()
        layout_general.setContentsMargins(0, 16, 0, 16)
        layout_general.addWidget(label_general, stretch=0)
        layout_general.addLayout(layout_autostart, stretch=0)
        layout_general.addLayout(layout_log_level, stretch=0)

        layout_home_assistant = QtWidgets.QVBoxLayout()
        layout_home_assistant.setContentsMargins(0, 16, 0, 16)
        layout_home_assistant.addWidget(label_home_assistant, stretch=0)
        layout_home_assistant.addLayout(layout_home_assistant_host, stretch=0)
        layout_home_assistant.addLayout(layout_home_assistant_port, stretch=0)
        layout_home_assistant.addLayout(layout_home_assistant_secure, stretch=0)
        layout_home_assistant.addLayout(layout_home_assistant_token, stretch=0)

        self.button_save = QtWidgets.QPushButton("Save")

        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(64, 16, 64, 16)
        layout.addWidget(label_heading, stretch=0, alignment=QtCore.Qt.AlignTop)
        layout.addLayout(layout_general, stretch=0)
        layout.addLayout(layout_home_assistant, stretch=0)
        layout.addWidget(self.button_save, stretch=0, alignment=QtCore.Qt.AlignBottom)

        self.button_save.clicked.connect(self.save)  # type: ignore

    # pylint: disable=invalid-name
    def closeEvent(
        self,
        event: QtGui.QCloseEvent,
    ) -> None:
        """Close the window instead of closing the app"""
        event.ignore()
        self.hide()

    @QtCore.Slot()
    def save(self):
        """Save and close the window"""
        self._settings.set(SETTING_AUTOSTART, str(self.input_autostart.isChecked()))
        self._settings.set(SETTING_LOG_LEVEL, str(self.input_log_level.text()))
        self._settings.set(
            SETTING_HOME_ASSISTANT_SECURE,
            str(self.input_home_assistant_secure.isChecked()),
        )
        self._settings.set(
            SETTING_HOME_ASSISTANT_HOST, str(self.input_home_assistant_host.text())
        )
        self._settings.set(
            SETTING_HOME_ASSISTANT_PORT, str(self.input_home_assistant_port.text())
        )
        self._settings.set_secret(
            SECRET_HOME_ASSISTANT_TOKEN, str(self.input_home_assistant_token.text())
        )
        self.close()
        self._callback("settings_updated")
