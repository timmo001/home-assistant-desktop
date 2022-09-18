"""Home Assistant Desktop: Main"""
from __future__ import annotations

import asyncio
import logging

import typer

from ._version import __version__
from .const import MESSAGE_STATE_CHANGED, SETTING_LOG_LEVEL
from .database import Database
from .homeassistant import HomeAssistant
from .logger import setup_logger
from .settings import Settings

app = typer.Typer()
database = Database()
settings = Settings(database)


async def setup() -> None:
    """Setup"""
    logger.info("Setup")
    await homeassistant.connect()
    await homeassistant.listen()


async def setup_complete() -> None:
    """Setup complete"""
    logger.info("Setup complete")
    await homeassistant.subscribe_events(MESSAGE_STATE_CHANGED)
    # homeassistant.subscribed_entities: list[str] = [
    #     subscribed_entity.entity_id
    #     for subscribed_entity in self._database.get_data(SubscribedEntities)
    # ]
    # homeassistant.id_states = await self.subscribe_entities(self.subscribed_entities)


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
