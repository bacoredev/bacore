"""FastHTML web interface tests."""
import pytest
from bacore.domain.source_code import ModuleModel
from bacore.interfaces.web_fasthtml import Documentation, docs_path, readme_page
from starlette.requests import Request
from pathlib import Path
from random import choice


def test_readme_page():
    assert isinstance(readme_page(title="BACore", readme_file=Path('README.md')), tuple)


@pytest.mark.parametrize("file_path, package_root, url", [
                             ('python/bacore/__init__.py', 'bacore', 'docs'),
                             ('python/bacore/domain/source_code.py', 'bacore', 'docs/domain/source-code'),
                             ('tests/domain/test_source_code.py', 'tests', 'docs/domain/test-source-code'),
                         ])
def test_docs_path(file_path, package_root, url):
    src_module = ModuleModel(path=Path(file_path), package_root=package_root)
    docs_url = docs_path(module=src_module, base_url='docs', package_root=package_root)

    assert docs_url == url


class TestDocumentation:
    docs = Documentation(path=Path('python/bacore'),
                         package_root='bacore',
                         base_url='docs')

    def test_docs_tree(self):
        url = choice(list(self.docs.docs_tree().keys()))
        assert isinstance(url, str), url
        assert isinstance(self.docs.docs_tree().get(url), ModuleModel), self.docs.docs_tree()