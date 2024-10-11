"""Test cases for BACore documentation with FastHTML."""
import inspect
import pytest
from bacore.interactors import source_code_reader
from bacore.interactors.file_handler import get_files_in_dir
from hypothesis import given, strategies as st
from pathlib import Path
from random import choice
from types import ModuleType


@pytest.fixture(scope="session")
def fixt_python_src_file_path() -> str:
    try:
        files = get_files_in_dir(directory="python/bacore/", recursive=True, pattern="[a-z]*.py")
    except FileNotFoundError:
        raise FileNotFoundError("No files found at path")

    src_file = choice(files)
    src_file_parts = src_file.parts
    src_file_path = '.'.join(src_file_parts)[7:-3]  # Remove "python" and ".py"

    return src_file_path


def test_get_module_from_name():
    """Import the "bacore.config" module."""
    config_module = source_code_reader.get_module_from_name("bacore.domain.settings")
    assert isinstance(config_module, ModuleType)


@given(st.text())
def test_neg_get_module_from_name(module_name):
    """Import a module from a text string generated by hypothesis."""
    with pytest.raises((ImportError, TypeError, ValueError)):
        source_code_reader.get_module_from_name(module_name)


def test_is_member_of_module():
    """Verify that an object is a member of the module it is created in."""
    settings_module = source_code_reader.get_module_from_name("bacore.domain.settings")
    assert source_code_reader.is_member_of_module(member=settings_module.Project, module_name="bacore.domain.settings")


def test_neg_is_member_of_module():
    """Verify that an object is not a member of the module it is created in."""
    files_module = source_code_reader.get_module_from_name("bacore.domain.files")
    assert not source_code_reader.is_member_of_module(member=files_module.TOML, module_name="bacore.domain.settings")


def test_get_module_members(fixt_python_src_file_path):
    """Verify that all members of a module does belong to the module."""
    module_name = fixt_python_src_file_path
    module_file = source_code_reader.get_module_from_name(module_name).__file__

    members = source_code_reader.get_module_members(module_name)
    for member in members:
        assert inspect.getfile(member) == module_file


def test_srcf_with_dir():
    with pytest.raises(ValueError):
        source_code_reader.SrcF(path=Path('python/bacore/domain/'))


def test_srcf_module_name():
    settings_file = source_code_reader.SrcF(path=Path('python/bacore/domain/settings.py'))
    assert settings_file.name == "settings"


def test_srcf_init_module_name():
    init_file = source_code_reader.SrcF(path=Path('python/bacore/__init__.py'))
    assert init_file.name == "bacore"


def test_srcf_members():
    settings_file = source_code_reader.SrcF(path=Path('python/bacore/domain/settings.py'))
    assert settings_file.members() == ['']