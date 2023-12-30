"""Configuration for the domain layer."""
import platform
from pathlib import Path
from pydantic import field_validator
from pydantic.dataclasses import dataclass


@dataclass
class System:
    """System configurations.

    Attributes:
        os: The operating system.
    """

    os = platform.system()


@dataclass
class Project:
    """Project configurations.

    Attributes:
        name: The name of the project.
        root_path: The path to the project.
    """

    name: str
    root_path: Path = Path.cwd()

    @field_validator("name")
    @classmethod
    def name_must_not_contain_spaces(cls, v: str) -> str:
        """Validate that the name does not contain spaces."""
        if " " in v:
            raise ValueError("No spaces allowed in project name.")
        return v
