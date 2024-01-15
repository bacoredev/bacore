"""CLI created with Typer."""
from bacore.interactors import install, retrieve
from rich import print
from typer import Exit
from typing import Protocol


class File(Protocol):
    """File protocol."""

    def read_content(self) -> dict:
        """Read name content."""
        ...


def verify_programs_installed(list_of_programs: list[str]):
    """Check if a list of programs are installed."""
    programs_not_installed = 0

    for program in list_of_programs:
        if install.command_on_path(program) is False:
            programs_not_installed += 1
            print(f'{program} is [red]not installed[/]. Install with: [blue]pip install bacore\\[cli\\][/]')

    if programs_not_installed > 0:
        raise Exit(code=1)
