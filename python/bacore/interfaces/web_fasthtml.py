"""FastHTML web interface."""
from bacore.domain.source_code import DirectoryModel, ModuleModel
from bacore.interactors.file_handler import read_markdown_file
from fasthtml.common import A, Div, Li, P, Ul, Titled
from pathlib import Path
from typing import Callable, Optional


def readme_page(title: str, readme_file: Path) -> Titled:
    return Titled(title, Div(read_markdown_file(file=readme_file, skip_title=True), cls='marked'))


def docs_path(module: ModuleModel, base_url: str, package_root: Optional[str] = None) -> str:
    """Create documentation web url path for module."""

    if not package_root:
        package_root = ''

    package_root_char = len(package_root)
    package_char = package_root_char + 1 if package_root != '' else 0
    url_without_package_root = module._module_path[package_char:]

    url_without_init = url_without_package_root.replace('__init__', '')

    url_with_hyphen = url_without_init.replace('_', '-')
    url_with_slashes = url_with_hyphen.replace('.', '/')

    raw_url = base_url + '/' + url_with_slashes

    url = raw_url[:-1] if raw_url.endswith('/') else raw_url

    return url


def map_module_path_to_module(directory_model: DirectoryModel, base_url: str, package_root: Optional[str] = None) -> dict[str, ModuleModel]:
    """Collect all modules with their paths relative to the package_root.

    Parameters
        directory_model: The directory model to traverse
        package_root: The package to be considered as base package.
    """

    path_module_mappings = {
        docs_path(module=module, base_url=base_url, package_root=package_root) : module.model_copy()
        for module in directory_model.modules
    }

    for subdirectory in directory_model.directories:
        path_module_mappings.update(map_module_path_to_module(directory_model=subdirectory, package_root=package_root, base_url=base_url))

    return path_module_mappings


class Documentation(DirectoryModel):
    """Documentation pages for project."""

    base_url: str

    def docs_tree(self) -> dict[str, ModuleModel]:
        if not self.package_root:
            self.package_root = ""
        url_module_mappings = map_module_path_to_module(directory_model=self, package_root=self.package_root, base_url=self.base_url)
        return url_module_mappings
