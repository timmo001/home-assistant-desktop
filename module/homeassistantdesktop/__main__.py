"""Home Assistant Desktop: Main"""
from __future__ import annotations

import asyncio
import logging
import sys

import typer

from ._version import __version__
from .autostart import autostart_disable, autostart_enable
from .base import Base
from .const import (
    MESSAGE_STATE_CHANGED,
    SETTING_AUTOSTART,
    SETTING_HOME_ASSISTANT_SUBSCRIBED_ENTITIES,
    SETTING_LOG_LEVEL,
)
from .database import Database
from .exceptions import (
    AuthenticationException,
    ConnectionClosedException,
    ConnectionErrorException,
)
from .gui import GUI
from .homeassistant import HomeAssistant
from .logger import setup_logger
from .settings import Settings
from .shortcut import create_shortcuts


class Main(Base):
    """Main"""

    def __init__(self) -> None:
        """Initialize"""
        super().__init__()
        self._cleaning = False
        self._homeassistant = HomeAssistant(database, settings, self.setup_complete)
        self._gui = GUI(self._callback, settings, self._homeassistant)

    def _callback(
        self,
        command: str,
    ) -> None:
        """Callback"""
        self._logger.info("Callback: %s", command)
        if command == "exit":
            self.exit()
        elif command == "settings_updated":
            self._logger.info("Settings updated")
            self.setup()

    def exit(self) -> None:
        """Exit"""
        self._logger.info("Exit application")
        self.cleanup()
        if loop is not None and loop.is_running():
            loop.stop()
        sys.exit(0)

    def cleanup(self) -> None:
        """Cleanup"""
        self._logger.info("Cleanup")
        self._cleaning = True
        self._gui.cleanup()
        loop.create_task(self._homeassistant.disconnect())
        self._cleaning = False

    def setup(self) -> None:
        """Setup"""
        if self._cleaning:
            return

        self._logger.info("Setup")

        self._gui.setup()
        loop.create_task(self.setup_home_assistant())

    async def setup_home_assistant(
        self,
        attempt: int = 1,
    ) -> None:
        """Setup Home Assistant"""
        self._logger.info("Setup Home Assistant: %s", attempt)
        if attempt > 3:
            self._logger.error(
                "Exceeded 3 attempts to setup application. Exiting now.."
            )
            sys.exit(1)

        try:
            await self._homeassistant.connect()
            attempt = 1
            await self._homeassistant.listen()
        except ConnectionClosedException as exception:
            self._logger.error("Home Assistant connection closed: %s", exception)
            if not self._cleaning:
                self._logger.info("Retrying in 5 seconds..")
                await asyncio.sleep(5)
                await self.setup_home_assistant(attempt + 1)
        except (AuthenticationException, ConnectionErrorException) as exception:
            self._logger.error("Home Assistant connection error: %s", exception)

    async def setup_complete(self) -> None:
        """Setup complete"""
        self._logger.info("Setup complete")
        await self._homeassistant.subscribe_events(MESSAGE_STATE_CHANGED)

        subscribed_entities = settings.get(SETTING_HOME_ASSISTANT_SUBSCRIBED_ENTITIES)
        self._logger.info("Subscribed entities: %s", subscribed_entities)
        if subscribed_entities is not None and isinstance(subscribed_entities, list):
            self._homeassistant.subscribed_entities = subscribed_entities


app = typer.Typer()


@app.command(name="main", short_help="Run main application")
def main() -> None:
    """Run main application"""
    typer.secho("Starting main application", fg=typer.colors.GREEN)

    autostart = settings.get(SETTING_AUTOSTART)
    logger.info("Autostart enabled: %s", autostart)
    if autostart:
        autostart_enable()
    else:
        autostart_disable()

    create_shortcuts()

    main_app.setup()
    loop.run_forever()


@app.command(name="version", short_help="Module Version")
def version() -> None:
    """Module Version"""
    typer.secho(__version__.public(), fg=typer.colors.CYAN)


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    database = Database()
    settings = Settings(database)
    main_app = Main()

    LOG_LEVEL = str(settings.get(SETTING_LOG_LEVEL))
    setup_logger(LOG_LEVEL, "homeassistantdesktop")
    logger = logging.getLogger(f"homeassistantdesktop.{__name__}")

    app()
