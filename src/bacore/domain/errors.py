"""Module for handling exceptions."""
from pydantic import ValidationError


class PydValErrInfo:
    """Information from pydantic ValidationError."""

    @staticmethod
    def error_msg(e: ValidationError) -> str:
        """Error message from pydantic ValidationError."""
        return repr(e.errors()[0]["ctx"]["error"]).split("'")[1]  # TODO: Fix to handle "'" in error message.

    @staticmethod
    def input(e: ValidationError) -> str:
        """Input value, as it is read by, pydantic ValidationError."""
        return e.errors()[0]["input"]
