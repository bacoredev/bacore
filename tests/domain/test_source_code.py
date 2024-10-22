"""Test cases for domain.source_code entities."""
from bacore.domain.source_code import ClassModel, DirectoryModel, FunctionModel, ModuleModel
from pathlib import Path
from random import choice
from types import ModuleType
from typing import Callable


class TestDirectoryModel:
    src_dir = DirectoryModel(path=Path('python/bacore'), package_root='bacore')

    def test_path(self):
        assert self.src_dir.path == Path('python/bacore')

    def test_name(self):
        assert self.src_dir.name == 'bacore', self.src_dir

    def test_src_files(self):
        module = choice(self.src_dir.modules)
        assert isinstance(module, ModuleModel), self.src_dir


class TestModuleModel:
    module = ModuleModel(path=Path('python/bacore/domain/source_code.py'), package_root="bacore")
    module_functions = ModuleModel(path=Path('python/bacore/interactors/source_code_reader.py'), package_root="bacore")
    init_module = ModuleModel(path=Path('python/bacore/__init__.py'), package_root='bacore')

    def test_path(self):
        assert self.module.path == Path('python/bacore/domain/source_code.py')
        assert self.init_module.path == Path('python/bacore/__init__.py')

    def test_module_path(self):
        assert self.module._module_path == 'bacore.domain.source_code'
        assert self.init_module._module_path == 'bacore.__init__'

    def test_as_module(self):
        assert isinstance(self.module._as_module(), ModuleType)
        assert isinstance(self.init_module._as_module(), ModuleType)

    def test_name(self):
        assert self.module.name == 'source_code', self.src_file.name
        assert self.init_module.name == 'bacore', self.src_file_init.name

    def test_doc(self):
        assert self.module.doc().splitlines()[0] == 'Source code entities.'
        assert self.init_module.doc().splitlines()[0] == '# BACore main init module'

    def test_functions(self):
        assert isinstance(self.module_functions.functions()[0], FunctionModel), self.module.functions()

    def test_classes(self):
        assert isinstance(self.module.classes()[0], ClassModel), self.module.classes()


class TestSrcClass:
    class_model = ModuleModel(path=Path('python/bacore/domain/source_code.py'), package_root="bacore").classes()[0]

    def test_klass(self):
        assert isinstance(self.class_model.klass, type), self.class_model.klass

    def test_name(self):
        assert self.class_model.name == "ClassModel"

    def test_doc(self):
        assert self.class_model.doc == "Python class model."


class TestSrcFunc:
    function_model = ModuleModel(path=Path('python/bacore/interactors/file_handler.py'), package_root="bacore").functions()[0]

    def test_func(self):
        assert isinstance(self.function_model.func, Callable)

    def test_name(self):
        assert self.function_model.name == 'delete_files'

    def test_doc(self):
        assert self.function_model.doc.splitlines()[0] == 'Delete files older than x days.'
