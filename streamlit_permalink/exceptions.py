"""
Exceptions for streamlit_permalink.
"""


class UrlParamError(Exception):
    """Exception raised for errors in URL parameter handling."""

    def __init__(
        self, message="URL parameter error", handler=None, url_value=None, url_key=None
    ):
        self.message = message
        self.handler = handler
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
