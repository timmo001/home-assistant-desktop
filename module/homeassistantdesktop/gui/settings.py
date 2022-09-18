"""Home Assistant Desktop: GUI - Settings"""
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
        settings: Settings,
    ):
        """Initialize"""
        super().__init__()

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
        label_heading.setFont(QtGui.QFont("Roboto Light", 48))

        label_autostart = QtWidgets.QLabel("Autostart")
        label_autostart.setFont(QtGui.QFont("Roboto Regular", 24))
        self.input_autostart = QtWidgets.QCheckBox()
        self.input_autostart.setCheckState(
            QtCore.Qt.CheckState.Checked
            if setting_autostart
            else QtCore.Qt.CheckState.Unchecked
        )
        layout_autostart = QtWidgets.QHBoxLayout()
        layout_autostart.addWidget(label_autostart)
        layout_autostart.addWidget(self.input_autostart)

        label_log_level = QtWidgets.QLabel("Log Level")
        label_log_level.setFont(QtGui.QFont("Roboto Regular", 24))
        self.input_log_level = QtWidgets.QLineEdit()
        self.input_log_level.setText(setting_log_level)
        layout_log_level = QtWidgets.QHBoxLayout()
        layout_log_level.addWidget(label_log_level)
        layout_log_level.addWidget(self.input_log_level)

        label_home_assistant_secure = QtWidgets.QLabel("Log Level")
        label_home_assistant_secure.setFont(QtGui.QFont("Roboto Regular", 24))
        self.input_home_assistant_secure = QtWidgets.QCheckBox()
        self.input_home_assistant_secure.setCheckState(
            QtCore.Qt.CheckState.Checked
            if setting_home_assistant_secure
            else QtCore.Qt.CheckState.Unchecked
        )
        layout_home_assistant_secure = QtWidgets.QHBoxLayout()
        layout_home_assistant_secure.addWidget(label_home_assistant_secure)
        layout_home_assistant_secure.addWidget(self.input_home_assistant_secure)

        label_home_assistant_host = QtWidgets.QLabel("Home Assistant Host")
        label_home_assistant_host.setFont(QtGui.QFont("Roboto Regular", 24))
        self.input_home_assistant_host = QtWidgets.QLineEdit()
        self.input_home_assistant_host.setText(setting_home_assistant_host)
        layout_home_assistant_host = QtWidgets.QHBoxLayout()
        layout_home_assistant_host.addWidget(label_home_assistant_host)
        layout_home_assistant_host.addWidget(self.input_home_assistant_host)

        label_home_assistant_port = QtWidgets.QLabel("Home Assistant Host")
        label_home_assistant_port.setFont(QtGui.QFont("Roboto Regular", 24))
        self.input_home_assistant_port = QtWidgets.QLineEdit()
        self.input_home_assistant_port.setText(setting_home_assistant_port)
        layout_home_assistant_port = QtWidgets.QHBoxLayout()
        layout_home_assistant_port.addWidget(label_home_assistant_port)
        layout_home_assistant_port.addWidget(self.input_home_assistant_port)

        label_home_assistant_token = QtWidgets.QLabel("Home Assistant Token")
        label_home_assistant_token.setFont(QtGui.QFont("Roboto Regular", 24))
        self.input_home_assistant_token = QtWidgets.QLineEdit()
        self.input_home_assistant_token.setText(secret_home_assistant_token)
        layout_home_assistant_token = QtWidgets.QHBoxLayout()
        layout_home_assistant_token.addWidget(label_home_assistant_token)
        layout_home_assistant_token.addWidget(self.input_home_assistant_token)

        self.button_save = QtWidgets.QPushButton("Save")

        self.layout = QtWidgets.QVBoxLayout(self)  # type: ignore
        self.layout.addWidget(label_heading, 0, QtCore.Qt.AlignTop)  # type: ignore
        self.layout.addLayout(layout_autostart, 0)  # type: ignore
        self.layout.addLayout(layout_log_level, 0)  # type: ignore
        self.layout.addLayout(layout_home_assistant_secure, 0)  # type: ignore
        self.layout.addLayout(layout_home_assistant_host, 0)  # type: ignore
        self.layout.addLayout(layout_home_assistant_port, 0)  # type: ignore
        self.layout.addLayout(layout_home_assistant_token, 0)  # type: ignore
        self.layout.addWidget(self.button_save, 0, QtCore.Qt.AlignBottom)  # type: ignore

        self.button_save.clicked.connect(self.save)  # type: ignore

    @QtCore.Slot()
    def save(self):
        """Save"""
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
