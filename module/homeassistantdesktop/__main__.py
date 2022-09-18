"""Home Assistant Desktop: Main"""
from __future__ import annotations

import asyncio
import logging

import typer

from ._version import __version__
from .const import SETTING_LOG_LEVEL
from .database import Database
from .homeassistant import HomeAssistant
from .logger import setup_logger
from .settings import Settings

app = typer.Typer()
database = Database()
settings = Settings(database)
homeassistant = HomeAssistant(settings)
loop = asyncio.new_event_loop()


async def setup() -> None:
    """Setup"""
    await homeassistant.connect()
    await homeassistant.listen()


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

    app()
