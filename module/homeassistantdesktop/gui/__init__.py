"""Home Assistant Desktop: GUI"""
import sys
from threading import Event, Thread

from PySide6 import QtWidgets
from qt_material import apply_stylesheet

from ..base import Base
from .settings import GUISettings


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

    def __init__(self):
        """Initialize"""
        super().__init__()
        self._application = None
        self._stopping = False

        self.gui_settings = None

    def _setup(self):
        """Setup"""
        self._logger.info("Setup GUI")

        self._application = QtWidgets.QApplication()
        apply_stylesheet(self._application, theme="dark_cyan.xml")

        self.gui_settings = GUISettings()
        self.gui_settings.resize(800, 600)
        self.gui_settings.show()

        sys.exit(self._application.exec())

    def setup(self) -> None:
        """Start the GUI"""
        self._thread = StoppableThread(target=self._setup)
        self._thread.start()
        self._stopping = False
