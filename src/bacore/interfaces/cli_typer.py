"""CLI created with Typer."""
from bacore.domain import files, system
from bacore.interactors import retrieve, verify
from rich import print
from pathlib import Path
from typer import Exit


class ProjectInfo:
    """Project information."""

    def __init__(self, pyproject_file: Path):
        """Initialize."""
        self._pyproject_file_toml_object = files.TOML(path=pyproject_file)
        self._project_info = retrieve.file_as_dict(file=self._pyproject_file_toml_object)

    @property
    def name(self) -> str:
        """Project name."""
        return self._project_info["project"]["name"]

    @property
    def version(self) -> str:
        """Project version."""
        return self._project_info["project"]["version"]

    @property
    def description(self) -> str:
        """Project description."""
        return self._project_info["project"]["description"]


def verify_programs_installed(list_of_programs: list[system.CommandLineProgram]):
    """Check if a list of command line programs are installed."""
    programs_not_installed = 0

    for program in list_of_programs:
        if verify.command_on_path(program) is False:
            programs_not_installed += 1
            print(f'{program} is [red]not installed[/]. Install with: [blue]pip install bacore\\[cli\\][/]')

    if programs_not_installed > 0:
        raise Exit(code=1)
