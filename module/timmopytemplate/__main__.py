"""Python Template: Main"""
from __future__ import annotations

import typer

from ._version import __version__

app = typer.Typer()


@app.command(name="hello", short_help="Say Hello World")
def hello_world() -> None:
    """Say Hello World"""
    typer.secho("Hello world", fg=typer.colors.GREEN)


@app.command(name="version", short_help="Module Version")
def version() -> None:
    """Module Version"""
    typer.secho(__version__.public(), fg=typer.colors.CYAN)


if __name__ == "__main__":
    app()
