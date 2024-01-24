"""Retrieve Functionality Module (the "get" word feels overloaded)."""
import platform
from bacore.domain import config
from typing import Protocol, runtime_checkable


@runtime_checkable
class SupportsRetrieveDict(Protocol):
    """Protocol for retrieval of file content as dict."""

    def data_to_dict(self) -> dict:
        """Content as dictionary."""
        ...


def file_as_dict(file: SupportsRetrieveDict) -> dict:
    """Content as dictionary."""
    return file.data_to_dict()


def system_information(func: callable = platform.system()) -> config.SystemInfo:
    """Retrieve system information."""
    info = config.SystemInfo(os=func)
    return info