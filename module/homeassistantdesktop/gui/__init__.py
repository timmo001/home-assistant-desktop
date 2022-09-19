"""Home Assistant Desktop: GUI"""
from collections.abc import Callable
from threading import Event, Thread
from typing import Optional
from webbrowser import open_new_tab

from PySide6 import QtWidgets
from qt_material import apply_stylesheet

from ..base import Base
from ..homeassistant import HomeAssistant
from ..settings import Settings
from .settings import GUISettings
from .tray import GUITray


class StoppableThread(Thread):
    """Thread class with a stop() method. The thread itself has to check
    regularly for the stopped() condition."""

    def __init__(
        self,
        *args,
        **kwargs,
    ) -> None:
        """Initialize the thread."""
        super().__init__(*args, **kwargs)
        self._stop_event = Event()

    def stop(self) -> None:
        """Stop the thread."""
        self._stop_event.set()

    def stopped(self) -> bool:
        """Return if the thread is stopped."""
        return self._stop_event.is_set()


class GUI(Base):
    """GUI"""

    def __init__(
        self,
        callback: Callable[[str], None],
        settings: Settings,
        homeassistant: HomeAssistant,
    ):
        """Initialize"""
        super().__init__()
        self._application: Optional[QtWidgets.QApplication] = None
        self._callback: Callable[[str], None] = callback
        self._homeassistant: HomeAssistant = homeassistant
        self._settings: Settings = settings
        self._stopping: bool = False
        self._thread: Optional[StoppableThread] = None

        self.gui_settings: Optional[GUISettings] = None
        self.gui_tray: Optional[GUITray] = None

    def _setup(self) -> int:
        """Setup"""
        self._logger.info("Setup GUI")

        if self._application is not None:
            self._logger.warning("GUI already setup")
            return 0

        self._application = QtWidgets.QApplication()
        apply_stylesheet(
            self._application,
            theme="dark_cyan.xml",
            extra={
                # Button colors
                "danger": "#dc3545",
                "warning": "#ffc107",
                "success": "#17a2b8",
                # Font
                "font_family": "Roboto",
                "font_size": "14px",
                # Density
                "density_scale": "0",
                # Button Shape
                "button_shape": "default",
            },
        )

        self.gui_tray = GUITray(
            self._tray_callback,
            self._settings,
            self._homeassistant,
        )
        self.gui_tray.update()
        self.gui_tray.show()

        self._logger.info("GUI setup complete")

        return self._application.exec()

    def _tray_callback(
        self,
        command: str,
    ) -> None:
        """Tray Callback"""
        self._logger.debug("Tray Callback: %s", command)
        if command == "exit":
            self.cleanup()
            self._callback(command)
        elif command == "homeassistant":
            self._logger.info("Open Home Assistant")
            open_new_tab(self._homeassistant.get_http_url())
        elif command == "settings":
            self._logger.info("Show settings")
            self.gui_settings = GUISettings(
                self._callback,
                self._settings,
                self._homeassistant,
            )
            self.gui_settings.resize(1080, 680)
            self.gui_settings.show()

    def cleanup(self) -> None:
        """Cleanup"""
        self._logger.info("Cleanup GUI")
        self._stopping = True
        if self.gui_settings is not None:
            self.gui_settings.close()
            self.gui_settings = None
        if self.gui_tray is not None:
            self.gui_tray.hide()
            self.gui_tray = None
        if self._application is not None:
            self._application.exit()
            self._application = None
        if self._thread is not None:
            self._thread.stop()
            self._thread = None
        self._stopping = False

    def setup(self) -> None:
        """Start the GUI"""
        if self._application is not None:
            self.cleanup()

        self._thread = StoppableThread(target=self._setup)
        self._thread.start()
        self._stopping = False
