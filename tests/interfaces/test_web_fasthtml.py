"""FastHTML web interface tests."""

import pytest
from bacore.domain.source_code import DirectoryModel, ModuleModel
from bacore.interfaces.web_fasthtml import (
    Documentation,
    docs_path,
    map_module_path_to_module,
    readme_page,
)
from pathlib import Path
from random import choice


def test_readme_page():
    assert isinstance(readme_page(title="BACore", readme_file=Path("README.md")), tuple)


@pytest.mark.parametrize(
    "file_path, package_root, expected_url",
    [
        ("python/bacore/__init__.py", "bacore", ""),
        ("python/bacore/domain/source_code.py", "bacore", "domain/source-code"),
        (
            "python/bacore/interactors/source_code_reader.py",
            "bacore",
            "interactors/source-code-reader",
        ),
        ("tests/conftest.py", "tests", "conftest"),
        ("tests/domain/test_source_code.py", "tests", "domain/test-source-code"),
    ],
)
def test_docs_path(file_path, package_root, expected_url):
    src_module = ModuleModel(path=Path(file_path), package_root=package_root)
    docs_url = docs_path(module=src_module)

    assert docs_url == expected_url


def test_map_module_path_to_module():
    src_dir = DirectoryModel(path=Path("python/bacore"), package_root="bacore")
    test_dir = DirectoryModel(path=Path("tests"), package_root="tests")

    src_mapping = map_module_path_to_module(directory_model=src_dir)
    src_path = choice(list(src_mapping.keys()))
    assert isinstance(src_mapping.get(src_path), ModuleModel), src_mapping.get(src_path)

    test_mapping = map_module_path_to_module(directory_model=test_dir)
    test_path = choice(list(test_mapping.keys()))
    assert isinstance(test_mapping.get(test_path), ModuleModel), test_mapping.get(test_path)


class TestDocumentation:
    src_docs = Documentation(path=Path("python/bacore"), package_root="bacore")
    test_docs = Documentation(path=Path("tests"), package_root="tests")

    def test_src_docs_tree(self):
        url = choice(list(self.src_docs.docs_tree().keys()))
        assert isinstance(url, str), url
        assert isinstance(self.src_docs.docs_tree().get(url), ModuleModel), self.src_docs.docs_tree()

    def test_test_docs_tree(self):
        url = choice(list(self.test_docs.docs_tree().keys()))
        assert isinstance(url, str), url
        assert isinstance(self.test_docs.docs_tree().get(url), ModuleModel), self.test_docs.docs_tree()
