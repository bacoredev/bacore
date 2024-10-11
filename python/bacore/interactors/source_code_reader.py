"""Source code reader module."""
import inspect
from importlib import import_module
from pathlib import Path
from types import ModuleType


def get_module_from_name(module_name: str) -> ModuleType:
    """Import a module by name.

    Parameters:
    - module_name: The name of the module to import.

    Returns:
    - The imported module.

    Example:
    - get_module_from_name('my_package.my_module')

    """
    if not module_name:
        raise ValueError("Module name cannot be empty")
    if module_name == "." or module_name == "..":
        raise TypeError("Module name should not only be one or two dots")
    try:
        return import_module(module_name)
    except ImportError:
        raise ImportError(f"Failed to import {module_name}")


def is_member_of_module(member, module_name: str) -> bool:
    """Check if a member is defined in a module.

    Use this function to filter members to include only those defined in your module.
    """
    member_file = inspect.getfile(member)
    module_file = get_module_from_name(module_name).__file__

    return member_file == module_file


def get_module_members(module_name: str):
    """Get members from a module.

    Parameters:
    - module_name: The name of the module.

    Returns:
    - A list of members defined in the module.
    """
    module = get_module_from_name(module_name)
    all_module_members = inspect.getmembers(module)

    module_members = [
        member for name, member in all_module_members
        if (inspect.isclass(member) or inspect.isfunction(member)) and is_member_of_module(member, module_name)
    ]

    return module_members


class SrcF:
    """Python source File."""

    def __init__(self, path: Path):
        self.path = path

    @property
    def path(self):
        return self._path

    @path.setter
    def path(self, value):
        if not value.is_file():
            raise ValueError(f'The path "{value}" is not a valid file.')
        self._path = value

    @property
    def name(self):
        if self.path.name.startswith('__init__.py'):
            return self.path.parent.name
        else:
            return self.path.name[:-3]

    def members(self):
        return [member for _, member in inspect.getmembers(self.path) if is_member_of_module(member, self.path)]

    def cls_members(self):
        """Class members of source file."""
        return ""


class SrcD:
    """Source directory."""

    def __init__(self, path: Path):
        self.path = path

    @property
    def name(self):
        return self.path.name
    # sub_folders: list[Path]
    # src_files: list[SrcF]


def list_files_in_dir(dir: Path, recursive: bool):
    """List all files in directory recursively as a tree."""
    pass