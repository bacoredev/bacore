"""Test cases for BACore documentation with FastHTML."""
from bacore.interactors.source_code_reader import SrcClass, SrcDir, SrcFile, SrcFunc
from pathlib import Path
from types import ModuleType
from typing import Callable


class TestSrcDdir:
    src_dir = SrcDir(path=Path('python/bacore'), package_root='bacore')

    def test_path(self):
        assert self.src_dir.path == Path('python/bacore')

    def test_name(self):
        assert self.src_dir.name == 'bacore'

    def test_sub_folders(self):
        for folder in self.src_dir.sub_folders:
            assert isinstance(folder, SrcDir)

    def test_src_files(self):
        for src_file in self.src_dir.src_files:
            assert isinstance(src_file, SrcFile)


class TestSrcFile:
    src_file = SrcFile(path=Path('python/bacore/interactors/source_code_reader.py'), package_root="bacore")
    src_file_init = SrcFile(path=Path('python/bacore/__init__.py'), package_root='bacore')

    def test_path(self):
        assert self.src_file.path == Path('python/bacore/interactors/source_code_reader.py')
        assert self.src_file_init.path == Path('python/bacore/__init__.py')

    def test_module_path(self):
        assert self.src_file._module_path == 'bacore.interactors.source_code_reader'
        assert self.src_file_init._module_path == 'bacore.__init__'

    def test_as_module(self):
        assert isinstance(self.src_file._as_module(), ModuleType)
        assert isinstance(self.src_file_init._as_module(), ModuleType)

    def test_name(self):
        assert self.src_file.name == 'source_code_reader', self.src_file.name
        assert self.src_file_init.name == 'bacore', self.src_file_init.name

    def test_doc(self):
        assert self.src_file.doc().splitlines()[0] == 'Source code reader module.'
        assert self.src_file_init.doc().splitlines()[0] == 'BACore main init module.'

    def test_classes(self):
        assert isinstance(self.src_file.classes()[0], SrcClass), self.src_file.classes()

    def test_functions(self):
        assert isinstance(self.src_file.functions()[0], SrcFunc), self.src_file.functions()


class TestSrcClass:
    src_class = SrcFile(path=Path('python/bacore/domain/settings.py'), package_root="bacore").classes()[0]

    def test_klass(self):
        assert isinstance(self.src_class.klass, type), self.src_class.klass

    def test_name(self):
        assert self.src_class.name == "Credentials"

    def test_doc(self):
        assert self.src_class.doc == "Credential details."

    def test_functions(self):
        assert isinstance(self.src_class.functions()[0], SrcFunc), self.src_class.functions()


class TestSrcFunc:
    src_func = SrcFile(path=Path('python/bacore/interactors/file_handler.py'), package_root="bacore").functions()[0]

    def test_func(self):
        assert isinstance(self.src_func.func, Callable)

    def test_name(self):
        assert self.src_func.name == 'delete_files'

    def test_doc(self):
        assert self.src_func.doc.splitlines()[0] == 'Delete files older than x days.'