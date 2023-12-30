"""Module for handling exceptions."""
from pydantic import ValidationError


class PydValErrInfo:
    """Pydantic validation information from ValidationError."""

    @staticmethod
    def error_msg(e: ValidationError) -> str:
        """Return the error message from a Pydantic ValidationError."""
        return repr(e.errors()[0]["ctx"]["error"]).split("'")[1]  # TODO: Fix to handle "'" in error message.

    @staticmethod
    def input(e: ValidationError) -> str:
        """Return the input from a Pydantic ValidationError."""
        return e.errors()[0]["input"]
