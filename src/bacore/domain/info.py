"""Config module for user specified settings and configurations."""
from pydantic import field_validator
from pydantic.dataclasses import dataclass
from typing import Optional


@dataclass
class Project:
    """Project information."""

    name: str
    version: Optional[str] = None
    description: Optional[str] = None

    @field_validator("name")
    @classmethod
    def name_must_not_contain_spaces(cls, v: str) -> str:
        """Validate that the name does not contain spaces."""
        if " " in v:
            raise ValueError("No spaces allowed in project name.")
        return v


@dataclass
class System:
    """System information."""

    os: str

    @field_validator("os")
    @classmethod
    def os_must_be_supported(cls, v: str) -> str:
        """Validate that the operating system is supported."""
        supported_oses = ["Darwin", "Linux", "Windows"]
        if v not in supported_oses:
            raise ValueError(f"Operating system '{v}' is not supported.")
        return v
