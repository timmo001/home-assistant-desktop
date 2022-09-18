"""Home Assistant Desktop: Install"""
import subprocess
import sys

import typer

app = typer.Typer()


@app.command()
def dev() -> None:
    """Install dev packages"""
    command = [
        sys.executable,
        "-m",
        "pip",
        "install",
        "--upgrade",
        "--pre",
    ]

    command = [
        *command,
        "homeassistantdesktop",
    ]

    print("Installing..")
    print(command)

    with subprocess.Popen(command) as process:
        process.wait()


@app.command()
def production() -> None:
    """Install production packages"""
    command = [
        sys.executable,
        "-m",
        "pip",
        "install",
        "--upgrade",
    ]

    command = [
        *command,
        "homeassistantdesktop",
    ]

    print("Installing..")
    print(command)

    with subprocess.Popen(command) as process:
        process.wait()


app()
