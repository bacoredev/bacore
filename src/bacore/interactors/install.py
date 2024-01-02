"""Installation Functionality Module."""
from shutil import which


def command_on_path(command: str) -> bool:
    """Check if CLI command is on path."""
    return which(command) is not None
