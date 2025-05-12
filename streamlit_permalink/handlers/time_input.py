from datetime import datetime, time

from .handler import WidgetHandler


def _parse_time_from_string(value: str) -> time:
    """Convert string time to time object with only hours and minutes."""
    return datetime.strptime(value, "%H:%M").time()


class TimeInputHandler(WidgetHandler):
    """
    Handler for time input widget URL state synchronization.
    """

    def update_bound_args(self) -> None:
        """
        Parse the URL value and update bound_args with the parsed value.
        """

        str_url_value = self.validate_single_url_value(self.url_value, allow_none=False)

        try:
            # Parse time value from URL in HH:MM format only
            parsed_value = _parse_time_from_string(str_url_value)
        except Exception as err:
            self.raise_url_error(
                f"Invalid time format for {self.handler_name} parameter '{self.url_key}': {str_url_value}. "
                f"Expected format: HH:MM.",
                err,
            )

        self.bound_args.arguments["value"] = parsed_value
