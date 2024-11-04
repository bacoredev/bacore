"""Source code reader module."""

import inspect
from bacore.domain.source_code import (
    ClassModel,
    DirectoryModel,
    FunctionModel,
    ModuleModel,
)
from pathlib import Path
from types import ModuleType
from typing import Literal, Optional


def get_objects(
    object_holder: ModuleType | type,
    object_holder_uri: str,
    match_object_type: Literal["class", "function", "class_and_function"],
) -> list[ClassModel | FunctionModel]:
    """Get members of a python object which are either functions or classes or both.

    Parameters
        object_holder: A module or a class.
        object_holder_module_path: Path to the object holding the with dot notation.
        match_object_type: The type of object type wished to be returned. Can be function, class or both.

    Returns
        SrcClass and/or SrcFunc.
    """
    match match_object_type:
        case "class":

            def member_filter(member):
                return inspect.isclass(member)

        case "function":

            def member_filter(member):
                return inspect.isfunction(member) or inspect.ismethod(member)

        case "class_and_function":

            def member_filter(member):
                return inspect.isclass(member) or inspect.isfunction(member) or inspect.ismethod(member)

        case _:
            raise ValueError(f"wrong value for match_object_type: {match_object_type}")

    return [
        (ClassModel(klass=member) if inspect.isclass(member) else FunctionModel(func=member))
        for _, member in inspect.getmembers(object_holder)
        if member_filter(member) and member.__module__.startswith(object_holder_uri)
    ]


def get_package_init_file(package_path: Path, package_root: Optional[str] = None) -> ModuleModel:
    """Return a file from a list of files if it meets the condition of having the name '__init__.py."""
    package = DirectoryModel(path=package_path, package_root=package_root)
    for module in package.modules:
        if module.name == "bacore":
            return module
    raise FileNotFoundError("No '__init__.py' file found in the package.")
