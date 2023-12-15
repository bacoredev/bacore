"""Provide CLI for all hax functionality."""
from typer import Option, Typer
from typing_extensions import Annotated

app = Typer(rich_markup_mode="rich", add_completion=False)


@app.command()
def init():
    """Initialize Bacore project in current directory.

    The command to initialize is just "bacore" until there are more commands.
    """
    print("This command is meant to initialize a Bacore project in the current directory.")