from datetime import datetime
from typing import Any, Union, Tuple
from datetime import date

from ..url_validators import validate_multi_url_values

from .handler import WidgetHandler


DateValue = Union[None, date, Tuple[date, ...]]


def get_date_value(value: Any) -> DateValue:
    """
    Convert a value ("today", datetime.date, datetime.datetime, str, or None) to a date value.
    """
    if isinstance(value, str):
        if value == "today":
            return date.today()
        return date.fromisoformat(value)
    if isinstance(value, (date, datetime)):
        return value
    if value is None:
        return None
    raise ValueError(
        f"Invalid value type for date input: {type(value)}. Expected str, datetime.date, datetime.datetime, or None."
    )


class DateInputHandler(WidgetHandler):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.is_range = isinstance(
            self.bound_args.arguments.get("value", "today"), (list, tuple)
        )

        self.min_value = get_date_value(self.bound_args.arguments.get("min_value"))
        self.max_value = get_date_value(self.bound_args.arguments.get("max_value"))

    def validate_bounds(self, date_value: Any) -> None:
        if self.min_value is not None and date_value < self.min_value:
            self.raise_url_error(
                f"Date {date_value} is before the minimum allowed date {self.min_value}."
            )
        if self.max_value is not None and date_value > self.max_value:
            self.raise_url_error(
                f"Date {date_value} is after the maximum allowed date {self.max_value}."
            )

    def sync_query_params(self) -> None:

        if not self.is_range:

            str_value = self.validate_single_url_value(self.url_value, allow_none=True)

            if str_value is None:
                self.bound_args.arguments["value"] = None
                return

            try:
                date_value = date.fromisoformat(str_value)
            except Exception as err:
                self.raise_url_error(
                    f"Invalid date format. Expected format: {str_value} YYYY-MM-DD.",
                    err,
                )

            self.validate_bounds(date_value)

            self.bound_args.arguments["value"] = date_value

        else:
            str_values = self.validate_multi_url_values(
                self.url_value, min_values=0, max_values=2, allow_none=True
            )
            try:
                date_values = tuple(date.fromisoformat(v) for v in str_values)
            except Exception as err:
                self.raise_url_error(
                    f"Invalid date format: {str_values}. Expected format: YYYY-MM-DD.",
                    err,
                )

            if len(date_values) == 2:
                start, end = date_values
                if start > end:
                    self.raise_url_error("Start date must be before end date.")

            for date_value in date_values:
                self.validate_bounds(date_value)

            self.bound_args.arguments["value"] = date_values

    @classmethod
    def verify_update_url_value(cls, value: Any) -> Any:
        if isinstance(value, (tuple, list)):
            if len(value) > 2:
                raise ValueError("Date input can only accept up to 2 values for range.")
            return tuple(get_date_value(v) for v in value)
        get_date_value(value)

    @classmethod
    def verify_get_url_value(cls, value: Any) -> Any:
        str_values = validate_multi_url_values(
            value, min_values=0, max_values=2, allow_none=True
        )
        try:
            date_values = tuple(date.fromisoformat(v) for v in str_values)
        except Exception as err:
            raise ValueError(
                f"Invalid date format: {str_values}. Expected format: YYYY-MM-DD.",
                err,
            )
        if len(date_values) == 2:
            start, end = date_values
            if start > end:
                raise ValueError("Start date must be before end date.")

        return date_values
