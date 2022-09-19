"""Home Assistant Desktop: GUI - Tray"""
import os
from typing import Callable

from PySide6 import QtCore, QtGui, QtWidgets

from ..settings import Settings


class GUITray(QtWidgets.QSystemTrayIcon):
    """GUI - Tray"""

    def __init__(
        self,
        settings: Settings,
        callback: Callable[[str], None],
    ):
        """Initialize"""
        super().__init__(
            QtGui.QIcon(os.path.join(os.path.dirname(__file__), "icon.png"))
        )

        self._callback = callback
        self._settings = settings

        self.activated.connect(self._on_activated)  # type: ignore

        self.menu = QtWidgets.QMenu()

        self.menu_settings = QtGui.QAction("Settings")
        self.menu_settings.triggered.connect(self._on_menu_settings)  # type: ignore

        self.menu.addAction(self.menu_settings)
        self.menu.addSeparator()

        self.setContextMenu(self.menu)

    @QtCore.Slot()
    def _on_activated(
        self,
        reason: int,
    ) -> None:
        """Handle the activated signal"""
        if reason == QtWidgets.QSystemTrayIcon.Trigger:
            self.contextMenu().popup(QtGui.QCursor.pos())

    @QtCore.Slot()
    def _on_menu_settings(self) -> None:
        """Menu Settings"""
        self._callback("settings")
