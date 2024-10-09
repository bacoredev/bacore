"""Source code reader module."""
import inspect
from importlib import import_module
from pathlib import Path
from types import ModuleType


# def get_module_names_recursive(package_path, base_package=''):
#     module_names = []
#     for entry in os.listdir(package_path):
#         full_path = os.path.join(package_path, entry)
#         if entry.endswith('.py') and not entry.startswith('__'):
#             module_name = entry[:-3]  # Remove '.py' extension
#             if base_package:
#                 module_name = f"{base_package}.{module_name}"
#             module_names.append(module_name)
#         elif os.path.isdir(full_path) and \
#              os.path.isfile(os.path.join(full_path, '__init__.py')):
#             subpackage = entry
#             if base_package:
#                 subpackage = f"{base_package}.{subpackage}"
#             module_names.append(subpackage)
#             # Recursively search in the subpackage
#             module_names.extend(get_module_names_recursive(full_path, subpackage))
#     return module_names


def get_modlue_names(package_path: Path, base_package=''):
    pass
    # module_names: set({})


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
