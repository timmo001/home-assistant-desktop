"""Home Assistant Desktop: Home Assistant"""

from .base import Base
from .settings import Settings


class HomeAssistant(Base):
    """Home Assistant"""

    def __init__(
        self,
        settings: Settings,
    ) -> None:
        """Initialize"""
        super().__init__()
        self._settings = settings
