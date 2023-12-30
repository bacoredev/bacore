"""Create CLI module."""
import subprocess as sup
from bacore.domain.config import Project
from bacore.domain.error_handling import PydValErrInfo
from pydantic import ValidationError
from rich import print
from shutil import which
from typer import Argument, Exit, Typer, prompt
from typing import Annotated

app = Typer(rich_markup_mode="rich")


@app.command(rich_help_panel="Create")
def project(name: Annotated[str, Argument(help="Name of project ([red]no spaces allowed[/]).")] = ''):
    """Create new project ([blue]with hatch[/])."""
    if which('hatch') is None:
        print('[red]hatch is not installed yet.[/] Install with: [blue]pip install bacore\\[cli\\][/blue]')
        raise Exit()

    if name == '':
        name = prompt("Enter project name")

    try:
        new_project = Project(name=name)
    except ValidationError as e:
        print(f'[red]{PydValErrInfo.error_msg(e)}[/red] Input was: "{PydValErrInfo.input(e)}"')
        raise Exit()

    print(f'Creating new project "{name}"[white]...[/]')
    sup.run(f'hatch new {name}', shell=True)
