"""Source code reader module."""
import inspect
from importlib import import_module
from pathlib import Path
from pydantic import BaseModel, computed_field, field_validator
from types import ModuleType
from typing import Callable, Literal, Optional


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


def get_sub_folders(folder: Path, package_root: Optional[str] = None) -> list['SrcDir']:
    return [
        SrcDir(path=dir_path, package_root=package_root) for dir_path in folder.glob('*')
        if dir_path.is_dir() and not (dir_path.name.startswith('__') or dir_path.name.startswith('.mypy_cache'))
    ]


def get_src_files(folder: Path, package_root: Optional[str] = None) -> list['SrcFile']:
    return [
        SrcFile(path=dir_path, package_root=package_root) for dir_path in folder.glob('*.py') if dir_path.is_file()
    ]


def get_objects(object_holder: ModuleType | type,
                object_holder_module_path: str,
                match_object_type: Literal['class', 'function', 'class_and_function']):
    """Get members of a python object which are either functions or classes or both.

    Parameters
        object_holder: A module or a class.
        object_holder_module_path: Path to the object holding the with dot notation.
        match_object_type: The type of object type wished to be returned. Can be function, class or both.

    Returns
        SrcClass and/or SrcFunc.
    """
    match match_object_type:
        case 'class':
            def member_filter(member): return inspect.isclass(member)
        case 'function':
            def member_filter(member): return inspect.isfunction(member) or inspect.ismethod(member)
        case 'class_and_function':
            def member_filter(member): return (inspect.isclass(member)
                                               or inspect.isfunction(member)
                                               or inspect.ismethod(member))
        case _:
            raise ValueError(f'wrong value for match_object_type: {match_object_type}')
    return [(SrcClass(klass=member) if inspect.isclass(member) else SrcFunc(func=member))
            for _, member in inspect.getmembers(object_holder)
            if member_filter(member) and member.__module__.startswith(object_holder_module_path)]


class SrcFunc(BaseModel):
    """Python source function."""
    func: Callable

    @computed_field
    @property
    def name(self) -> str:
        return self.func.__name__

    @computed_field
    @property
    def doc(self) -> str | None:
        return inspect.getdoc(self.func)


class SrcClass(BaseModel):
    """Python source class."""
    klass: type

    @computed_field
    @property
    def name(self) -> str:
        return self.klass.__name__

    @computed_field
    @property
    def doc(self) -> str | None:
        return inspect.getdoc(self.klass)

    def functions(self) -> list[SrcFunc]:
        """Get functions as members from module and type as 'SrcFunc' class."""
        return get_objects(object_holder=self.klass,
                           object_holder_module_path=self.klass.__module__, match_object_type="function")


class SrcFile(BaseModel):
    """Python source file."""
    path: Path
    package_root: Optional[str] = None

    @field_validator('path')
    @classmethod
    def path_must_be_file(cls, v):
        if not v.is_file():
            ValueError(f'path must point to a file, not {v}')
        return v

    @computed_field
    @property
    def _module_path(self) -> str:
        """Returns the path to the module with dot notation as a string and removes '.py'"""
        src_file_without_suffix = self.path.with_suffix("")
        src_file_parts = src_file_without_suffix.parts
        if self.package_root is None:
            return '.'.join(src_file_parts)
        else:
            src_root_index_start = src_file_parts.index(self.package_root)
            return '.'.join(src_file_parts[src_root_index_start:])

    def _as_module(self) -> ModuleType:
        try:
            return import_module(self._module_path)
        except ImportError:
            raise ImportError(f"Failed to import {self._module_path}")

    @computed_field
    @property
    def name(self) -> str:
        if self.path.name.startswith('__init__.py'):
            return self.path.parent.name
        else:
            return self.path.name[:-3]

    def doc(self) -> str | None:
        return self._as_module().__doc__

    def classes(self) -> list[SrcClass]:
        """Get the members of a module which belong to the file."""
        return get_objects(object_holder=self._as_module(),
                           object_holder_module_path=self._module_path,
                           match_object_type='class')

    def functions(self) -> list[SrcFunc]:
        """Class members of source file."""
        return get_objects(object_holder=self._as_module(),
                           object_holder_module_path=self._module_path,
                           match_object_type='function')


class SrcDir(BaseModel):
    """Source directory."""
    path: Path
    package_root: Optional[str] = None

    @computed_field
    @property
    def name(self) -> str:
        return self.path.name

    @computed_field
    @property
    def src_files(self) -> list[SrcFile]:
        return get_src_files(folder=self.path, package_root=self.package_root)

    @computed_field
    @property
    def sub_folders(self) -> list['SrcDir']:
        return get_sub_folders(folder=self.path, package_root=self.package_root)


def package_init_file(package_path: Path, package_root: Optional[str] = None) -> SrcFile:
    """Return a file from a list of files if it meets the condition of having the name '__init__.py."""
    package = SrcDir(path=package_path, package_root=package_root)
    for file in package.src_files:
        if file.name == 'bacore':
            return file
    raise FileNotFoundError("No '__init__.py' file found in the package.")