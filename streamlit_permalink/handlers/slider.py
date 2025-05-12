from datetime import datetime, date, time
from typing import Any

from .handler import WidgetHandler


VALID_TYPES = {int, float, datetime, date, time}


class SliderHandler(WidgetHandler):
    """
    Handler for slider widget URL state synchronization.
    """

    def __init__(self, *args, **kwargs):
        """
        Initialize the HandlerSlider instance.
        """
        super().__init__(*args, **kwargs)

        self.min_value = self.bound_args.arguments.get("min_value")
        self.max_value = self.bound_args.arguments.get("max_value")

        # default to int if not set
        self.value = self.bound_args.arguments.get("value")
        if self.value is None:
            self.value = self.bound_args.arguments.get("min_value")
        if self.value is None:
            self.value = 0

        self.is_range = False
        if isinstance(self.value, (list, tuple)):
            if len(self.value) == 2:
                self.is_range = True
            else:
                raise ValueError(
                    f"Invalid value for slider parameter: {self.value}. Expected a list or tuple of length 2."
                )

            # check that the two values are of the same type
            if type(self.value[0]) != type(self.value[1]):
                raise ValueError(
                    f"Invalid value for slider parameter: {self.value}. "
                    f"Expected a list or tuple of the same type."
                )

            self.value_type = type(self.value[0])
        else:
            self.value_type = type(self.value)

        if self.value_type not in VALID_TYPES:
            raise ValueError(
                f"Invalid value type for slider parameter: {self.value_type}. "
                f"Expected one of: {VALID_TYPES}"
            )

    def parse_value(self, value: Any) -> Any:

        if self.value_type == int:
            return int(value)
        if self.value_type == float:
            return float(value)
        if self.value_type == datetime:
            return datetime.strptime(value, "%Y-%m-%dT%H:%M:%S")
        if self.value_type == date:
            return datetime.strptime(value, "%Y-%m-%d").date()
        if self.value_type == time:
            return datetime.strptime(value, "%H:%M").time()
        raise ValueError(
            f"Unsupported value type: {self.value_type}. Expected one of: {VALID_TYPES}"
        )

    def check_bounds(self, value: Any) -> None:
        """
        Check if the value is within the bounds of min_value and max_value.
        """
        if self.min_value is not None and value < self.min_value:
            self.raise_url_error(
                f"Value {value} is less than min_value {self.min_value}."
            )
        if self.max_value is not None and value > self.max_value:
            self.raise_url_error(
                f"Value {value} is greater than max_value {self.max_value}."
            )

    def update_bound_args(self) -> None:
        """
        Parse the URL value and update bound_args with the parsed value.
        """

        if self.is_range:
            str_values = self.validate_multi_url_values(
                self.url_value, min_values=2, max_values=2, allow_none=False
            )
            parsed_values = [self.parse_value(v) for v in str_values]

            for v in parsed_values:
                self.check_bounds(v)

            if parsed_values[0] > parsed_values[1]:
                self.raise_url_error(
                    f"Start value {parsed_values[0]} is greater than end value {parsed_values[1]}."
                )

            self.bound_args.arguments["value"] = parsed_values

        else:
            str_value = self.validate_single_url_value(self.url_value, allow_none=False)
            parsed_value = self.parse_value(str_value)
            self.check_bounds(parsed_value)
            self.bound_args.arguments["value"] = parsed_value
