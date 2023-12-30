"""Provide CLI for all hax functionality."""
from bacore.cli import create
from typer import Typer

app = Typer(rich_markup_mode="rich", add_completion=False)
app.add_typer(create.app, name="create", help="Create something...")
