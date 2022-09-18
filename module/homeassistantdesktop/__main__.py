"""Home Assistant Desktop: Main"""
from __future__ import annotations

import typer

from ._version import __version__
from .database import Database
from .homeassistant import HomeAssistant
from .settings import Settings

app = typer.Typer()
database = Database()
settings = Settings(database)
homeassistant = HomeAssistant(settings)


@app.command(name="main", short_help="Run main application")
def main() -> None:
    """Run main application"""
    typer.secho("Hello world", fg=typer.colors.GREEN)


@app.command(name="version", short_help="Module Version")
def version() -> None:
    """Module Version"""
    typer.secho(__version__.public(), fg=typer.colors.CYAN)


if __name__ == "__main__":
    app()
