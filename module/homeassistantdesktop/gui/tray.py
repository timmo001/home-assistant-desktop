"""Home Assistant Desktop: GUI - Tray"""
from collections.abc import Callable
import os

from PySide6 import QtCore, QtGui, QtWidgets

from ..base import Base
from ..homeassistant import HomeAssistant
from ..settings import Settings


class GUITray(Base, QtWidgets.QSystemTrayIcon):
    """GUI - Tray"""

    def __init__(
        self,
        callback: Callable[[str], None],
        settings: Settings,
        homeassistant: HomeAssistant,
    ):
        """Initialize"""
        Base.__init__(self)
        QtWidgets.QSystemTrayIcon.__init__(
            self,
            QtGui.QIcon(os.path.join(os.path.dirname(__file__), "icon.png")),
        )

        self._callback = callback
        self._homeassistant = homeassistant
        self._settings = settings

        self._homeassistant.watch_subscribed_entities(self.update)

        self.activated.connect(self._on_activated)  # type: ignore

        self.menu = QtWidgets.QMenu()

        self.menu_settings = QtGui.QAction("Settings")
        self.menu_settings.triggered.connect(self._on_menu_settings)  # type: ignore

        self.menu_exit = QtGui.QAction("Exit")
        self.menu_exit.triggered.connect(self._on_menu_exit)  # type: ignore

        self.menu.addAction(self.menu_settings)
        self.menu.addSeparator()
        self.menu.addAction(self.menu_exit)

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
    def _on_menu_exit(self) -> None:
        """Menu Exit"""
        self._callback("exit")

    @QtCore.Slot()
    def _on_menu_settings(self) -> None:
        """Menu Settings"""
        self._callback("settings")

    def update(self) -> None:
        """Update"""
        self._logger.info("Update tray")
        if (
            self._homeassistant.states is not None
            and self._homeassistant.subscribed_entities is not None
            and len(self._homeassistant.subscribed_entities) > 0
        ):
            tooltip = ""
            for entity in self._homeassistant.subscribed_entities:
                state = self._homeassistant.states.get(entity)
                self._logger.info("State: %s", state)
                if state is not None:
                    if len(tooltip) > 0:
                        tooltip += "\n"
                    tooltip += (
                        f"{state['attributes']['friendly_name']}: {state['state']}"
                    )
                    unit_of_measurement = state["attributes"].get("unit_of_measurement")
                    if unit_of_measurement is not None:
                        tooltip += unit_of_measurement
                    self._logger.info(tooltip)

            # pixmap = QtGui.QPixmap(48, 48)
            # pixmap.fill(QtCore.Qt.transparent)
            # painter = QtGui.QPainter(pixmap)
            # painter.setRenderHint(QtGui.QPainter.Antialiasing)
            # painter.setPen(QtGui.QColor(255, 255, 255, 255))
            # painter.drawText(
            #     QtCore.QRect(0, 0, 148, 148),
            #     state["state"],
            # )
            # painter.end()

            # self.setIcon(QtGui.QIcon(pixmap))
            self.setToolTip(tooltip)
