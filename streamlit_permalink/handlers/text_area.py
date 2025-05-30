from typing import Any

from ..url_validators import validate_single_url_value
from .handler import WidgetHandler


class TextAreaHandler(WidgetHandler):
    """
    Handler for text area widget URL state synchronization.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.max_chars = self.bound_args.arguments.get("max_chars", None)

    def sync_query_params(self) -> None:

        # Get the validated single URL value
        value = self.validate_single_url_value(self.url_value, allow_none=True)

        if value is None:
            # If no URL value is provided, set value to None
            self.bound_args.arguments["value"] = None
            return

        # Check if the value exceeds the maximum characters limit
        if self.max_chars is not None and len(value) > self.max_chars:
            self.raise_url_error(
                f"Text exceeds maximum allowed characters: {len(value)} "
                f"characters provided, but limit is {self.max_chars}"
            )

        # Update bound arguments with validated value
        self.bound_args.arguments["value"] = value

    @classmethod
    def verify_update_url_value(cls, value: Any) -> Any:
        if not isinstance(value, str):
            raise ValueError(
                f"{cls.__name__} value must be a string, got {type(value)}"
            )
        return value

    @classmethod
    def verify_get_url_value(cls, value: Any) -> Any:
        """
        Validate the URL value for text area.
        """
        return [validate_single_url_value(value, allow_none=True)]
