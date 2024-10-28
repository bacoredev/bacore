"""FastHTML web interface."""
from bacore.domain.source_code import DirectoryModel, ModuleModel
from bacore.interactors.file_handler import read_markdown_file
from fasthtml.common import Div, H1, H2, H3, H4, Li, P, Ul, Titled
from pathlib import Path
from typing import Optional


def readme_page(title: str, readme_file: Path, skip_title: bool = True) -> Titled:
    """Markdown file rendered in HTML format. The title of the markdown file is skipped.

    Parameters
        `title`: Title of the page
        `readme_file`: The path to the markdown file to be renered.
        `skip_title`: If the title of the page should be skipped. Default is `True`.

    Returns
        A page as a FastHTML Titled page.
    """
    content = read_markdown_file(file=readme_file, skip_title=skip_title)
    return Titled(title, Div(content, cls='marked'))


def docs_path(module: ModuleModel, base_url: str, package_root: Optional[str] = None) -> str:
    """Create documentation web url path for module.

    package_offset is increased by 1 to remove the leading slash from the module path.
    """
    package_root = package_root or ''
    package_offset = len(package_root) + 1 if package_root else 0
    url = (module._module_path[package_offset:]
           .replace('__init__', '')
           .replace('_', '-')
           .replace('.', '/'))
    return f'{base_url}/{url}'.removesuffix('/')


def map_module_path_to_module(directory_model: DirectoryModel, base_url: str, package_root: Optional[str] = None
                              ) -> dict[str, ModuleModel]:
    """Collect all modules with their paths relative to the package_root.

    Parameters
        directory_model: The directory model to traverse
        package_root: The package to be considered as base package.
    """
    path_module_mappings = {
        docs_path(module, base_url, package_root): module.model_copy()
        for module in directory_model.modules
    }
    for subdirectory in directory_model.directories:
        path_module_mappings.update(map_module_path_to_module(subdirectory,  base_url, package_root,))
    return path_module_mappings


class Documentation(DirectoryModel):
    """Documentation pages for project."""

    base_url: str

    def docs_tree(self) -> dict[str, ModuleModel]:
        self.package_root = self.package_root or ''
        return map_module_path_to_module(directory_model=self,
                                         base_url=self.base_url,
                                         package_root=self.package_root)


def doc_page(doc_source: Documentation, url: str) -> Titled:
    """Dirty implementation of the Documentation (future) component.

    The **Module Classes** function has to be recursive in the same way as
    `map_path_to_module` in `interfaces/web_fasthtml` is.
    """
    module = doc_source.docs_tree().get(url)
    if module is None:
        raise ValueError(f'404 module "{url}" does not exist')

    funcs = module.functions()
    classes = module.classes()

    return Titled(module.name.title(),
                  Div(module.doc(), cls='marked'),
                  Div(
                      H1('Module Functions'),
                      Ul(*[Li(func.name.title()) for func in funcs]),
                      Div(*[(H2(func.name.title()), P(func.doc, cls='marked')) for func in funcs])
                  ) if funcs else '',
                  Div(
                      H1('Module Classes'),
                      Ul(*[Li(klass.name.title()) for klass in classes]),
                      Div(*[(H2(klass.name.title()), P(klass.doc, cls='marked'),
                          Div(
                              H3('Class Functions'),
                              Ul(*[Li(class_func.name.title()) for class_func in klass.functions()]),
                              Div(*[(H4(class_func.name.title()), P(class_func.doc, cls='marked')) for class_func in klass.functions()])
                              ) if klass.functions() else "",
                          Div(
                              H3('Sub-Classes'),
                              Ul(*[Li(sub_class.name.title()) for sub_class in klass.classes()]),
                              Div(*[(H4(sub_class.name.title()), P(sub_class.doc, cls='marked')) for sub_class in klass.classes()])
                              ) if klass.classes() else "",
                             ) for klass in classes])
                  ) if classes else ''
                  )