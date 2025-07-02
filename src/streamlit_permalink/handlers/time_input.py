"""Handler for time input widget URL state synchronization."""

from datetime import datetime, time
from typing import Any

from ..url_validators import validate_single_url_value_disallow_none
from .handler import WidgetHandler


def _parse_time_from_string(value: str) -> time:
    """Convert string time to time object with only hours and minutes."""

    return datetime.strptime(value, "%H:%M").time()


class TimeInputHandler(WidgetHandler):
    """Handler for time input widget URL state synchronization."""

    def sync_query_params(self) -> None:
        """Sync the query parameters with the widget state."""

        str_url_value = self.validate_single_url_value_disallow_none(self.url_value)

        try:
            # Parse time value from URL in HH:MM format only
            parsed_value = _parse_time_from_string(str_url_value)
        except Exception as err:
            self.raise_url_error(
                f"Invalid time format for {self.handler_name} parameter '{self.url_key}': {str_url_value}. "
                f"Expected format: HH:MM.",
                err,
            )
            raise RuntimeError("Unreachable")

        self.bound_args.arguments["value"] = parsed_value

    @classmethod
    def verify_update_url_value(cls, value: Any) -> Any:
        """Verify that the value is a valid time object."""

        if value == "now":
            return datetime.now().time()

        if isinstance(value, str):
            try:
                return _parse_time_from_string(value)
            except ValueError as err:
                raise ValueError(
                    f"Invalid time string format: {value}. Expected HH:MM."
                ) from err

        if not isinstance(value, (datetime.time, datetime.datetime)):
            raise ValueError(
                f"{cls.__name__} value must be a time object, got {type(value)}"
            )
        return value

    @classmethod
    def verify_get_url_value(cls, value: Any) -> Any:
        """Validate the URL value for time input."""

        return [validate_single_url_value_disallow_none(value)]
