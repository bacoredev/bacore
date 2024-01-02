"""Serve CLI module."""
import subprocess as sup
from bacore.domain.config import Project
from bacore.domain.errors import PydValErrInfo
from bacore.interfaces.cli import verify_programs_installed
from pydantic import ValidationError
from rich import print
from typer import Argument, Exit, Option, Typer, prompt
from typing import Annotated

app = Typer(rich_markup_mode="rich")


@app.command(rich_help_panel="Serve")
def documentation(project: Annotated[str, Argument(help="Name of project.")] = '',
                  port: Annotated[int, Option(help="Port to serve documentation on.")] = 8000):
    """Serve documentation with MkDocs for a project."""
    verify_programs_installed(['mkdocs'])

    if project == '':
        project = prompt("Enter project name")

    try:
        project = Project(name=project)
    except ValidationError as e:
        print(f'[red]{PydValErrInfo.error_msg(e)}[/red] Input was: "{PydValErrInfo.input(e)}"')
        raise Exit()

    print(f'Serving documentation for project "{project.name}"[white]...[/]')
    sup.run(f"cd {project.root_path} && mkdocs serve -a 127.0.0.1:{port} &", shell=True)
    sup.run(f'cd {project} && mkdocs serve', shell=True)

