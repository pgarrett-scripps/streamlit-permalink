"""
Exceptions for streamlit_permalink.
"""

from typing import Any, Optional


class UrlParamError(Exception):
    """Exception raised for errors in URL parameter handling."""

    def __init__(
        self,
        message: str = "URL parameter error",
        handler_name: Optional[str] = None,
        url_value: Optional[Any] = None,
        url_key: Optional[str] = None,
    ):
        self.message = message
        self.handler = handler_name
        self.url_value = url_value
        self.url_key = url_key
        super().__init__(self.message)

    def __str__(self):
        parts = [self.message]
        if self.handler:
            parts.append(f"handler: {self.handler}")
        if self.url_key:
            parts.append(f"url_key: {self.url_key}")
        if self.url_value:
            parts.append(f"url_value: {self.url_value}")
        return ", ".join(parts)
