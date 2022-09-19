"""Home Assistant Desktop: Main"""
from __future__ import annotations

import asyncio
import logging

import typer

from ._version import __version__
from .const import (
    MESSAGE_STATE_CHANGED,
    SETTING_HOME_ASSISTANT_SUBSCRIBED_ENTITIES,
    SETTING_LOG_LEVEL,
)
from .database import Database
from .exceptions import ConnectionClosedException, ConnectionErrorException
from .gui import GUI
from .homeassistant import HomeAssistant
from .logger import setup_logger
from .settings import Settings

app = typer.Typer()
database = Database()
settings = Settings(database)


async def setup(attempt: int = 1) -> None:
    """Setup"""
    logger.info("Setup: %s", attempt)
    if attempt > 3:
        logger.error("Exceeded 3 attempts to setup application. Exiting now..")
        exit(1)
    try:
        await homeassistant.connect()
        attempt = 1
        await homeassistant.listen()
    except ConnectionClosedException as exception:
        logger.error("Connection closed: %s", exception)
        logger.info("Retrying in 5 seconds..")
        await asyncio.sleep(5)
        await setup(attempt + 1)
    except ConnectionErrorException as exception:
        logger.error("Connection error: %s", exception)
        logger.info("Retrying in 5 seconds..")
        await asyncio.sleep(5)
        await setup(attempt + 1)


async def setup_complete() -> None:
    """Setup complete"""
    logger.info("Setup complete")
    await homeassistant.subscribe_events(MESSAGE_STATE_CHANGED)

    subscribed_entities = settings.get(SETTING_HOME_ASSISTANT_SUBSCRIBED_ENTITIES)
    logger.info("Subscribed entities: %s", subscribed_entities)
    if subscribed_entities is not None and isinstance(subscribed_entities, list):
        homeassistant.subscribed_entities = subscribed_entities
    gui = GUI(settings, homeassistant)
    gui.setup()


@app.command(name="main", short_help="Run main application")
def main() -> None:
    """Run main application"""
    typer.secho("Starting main application", fg=typer.colors.GREEN)
    asyncio.run(setup())


@app.command(name="version", short_help="Module Version")
def version() -> None:
    """Module Version"""
    typer.secho(__version__.public(), fg=typer.colors.CYAN)


if __name__ == "__main__":
    LOG_LEVEL = str(settings.get(SETTING_LOG_LEVEL))
    setup_logger(LOG_LEVEL, "homeassistantdesktop")
    logging.getLogger("zeroconf").setLevel(logging.ERROR)
    asyncio.new_event_loop()
    homeassistant = HomeAssistant(database, settings, setup_complete)
    logger = logging.getLogger(f"homeassistantdesktop.{__name__}")

    app()
