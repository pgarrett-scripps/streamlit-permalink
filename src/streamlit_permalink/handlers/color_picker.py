"""Handler for color picker widget URL state synchronization."""

from typing import Any

from ..url_validators import (
    is_valid_color,
    validate_color,
    validate_single_url_value_disallow_none,
)
from .handler import WidgetHandler


class ColorPickerHandler(WidgetHandler):
    """Handler for color picker widget URL state synchronization."""

    def validate_color(self, value: str) -> str:
        """Validate that the value is a valid color."""

        try:
            return validate_color(value)
        except ValueError as err:
            self.raise_url_error(
                f"Invalid color format: {value}. Expected format: #RRGGBB.",
                err=err,
            )

        raise RuntimeError("Unreachable")

    def sync_query_params(self) -> None:
        """Sync color picker value with URL parameter."""

        str_value: str = self.validate_single_url_value_disallow_none(self.url_value)
        color_value: str = self.validate_color(str_value)
        self.bound_args.arguments["value"] = color_value

    @classmethod
    def verify_update_url_value(cls, value: Any) -> Any:
        """Verify that the value is a valid color."""

        if not isinstance(value, str):
            raise ValueError(f"Color value must be a string, got {type(value)}")
        if not is_valid_color(value):
            raise ValueError(
                f"Invalid color format: {value}. Expected format: #RRGGBB."
            )
        return value

    @classmethod
    def verify_get_url_value(cls, value: Any) -> Any:
        """Validate the URL value for color picker."""

        return [
            validate_color(validate_single_url_value_disallow_none(url_value=value))
        ]
