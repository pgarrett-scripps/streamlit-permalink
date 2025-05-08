from datetime import datetime
from typing import Any, Union, Optional, List, Tuple
from datetime import date

from ..utils import _validate_multi_url_values, validate_single_url_value
from .handler import HandleWidget
from ..exceptions import UrlParamError


DateValue = Union[None, date, Tuple[date, ...]]


def get_date_value(value: Any) -> DateValue:
    """
    Convert a value ("today", datetime.date, datetime.datetime, str, or None) to a date value.
    """
    if isinstance(value, str):
        if value == "today":
            return date.today()
        return date.fromisoformat(value)
    elif isinstance(value, (date, datetime)):
        return value
    elif value is None:
        return None
    else:
        raise UrlParamError(f"Invalid date value: {value}. Expected a date or 'today'.")
    

class HandlerDateInput(HandleWidget):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.is_range = isinstance(
            self.bound_args.arguments.get("value", "today"), (list, tuple)
        )

        """
        ("today", datetime.date, datetime.datetime, str, or None)
        """
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

    def update_bound_args(self) -> None:

        if not self.is_range:

            str_value = self.validate_single_url_value(allow_none=True)

            if str_value is None:
                self.bound_args.arguments["value"] = None
                return

            try:
                date_value = date.fromisoformat(str_value)
            except Exception as err:
                self.raise_url_error(f"Invalid date format. Expected format: YYYY-MM-DD.", err)

            self.validate_bounds(date_value)

            self.bound_args.arguments["value"] = date_value

        else:
            str_values = self.validate_multi_url_values(min_values=0, max_values=2, allow_none=True)
            try:
                date_values = tuple(date.fromisoformat(v) for v in str_values)
            except Exception as err:
                self.raise_url_error(f"Invalid date format. Expected format: YYYY-MM-DD.", err)
                
            if len(date_values) == 2:
                start, end = date_values
                if start > end:
                    self.raise_url_error(
                        "Start date must be before end date."
                    )

            for date_value in date_values:
                self.validate_bounds(date_value)

            self.bound_args.arguments["value"] = date_values