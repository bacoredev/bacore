"""BACore CLI interface."""
from bacore.interactors.install import command_on_path
from rich import print
from typer import Exit


def verify_programs_installed(list_of_programs: list[str]):
    """Check if a list of programs are installed."""
    programs_not_installed = 0

    for program in list_of_programs:
        if command_on_path(program) is False:
            programs_not_installed += 1
            print(f'{program} is [red]not installed[/]. Install with: [blue]pip install bacore\\[cli\\][/]')

    if programs_not_installed > 0:
        Exit()
