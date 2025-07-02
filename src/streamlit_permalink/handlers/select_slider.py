"""Handler for select slider widget."""

from typing import Any, List

from ..url_validators import validate_multi_url_values
from ..utils import (
    validate_multi_options,
)
from .handler import WidgetHandler


class SelectSliderHandler(WidgetHandler):

    def __init__(self, *args: Any, **kwargs: Any):
        """Initialize the HandlerSelectSlider instance."""

        super().__init__(*args, **kwargs)
        # Get and validate options
        options = self.bound_args.arguments.get("options", None)
        self.options: List[Any]
        if options is None:
            self.options = []
        else:
            self.options = options

        self.str_options: List[str] = validate_multi_options(
            self.options, self.handler_name
        )

        # Get value
        self.value: Any = self.bound_args.arguments.get("value", self.options[0])

        self.is_range_slider = False
        if isinstance(self.value, (tuple, list)):
            if len(self.value) != 2:
                raise ValueError(
                    f"Invalid value for {self.handler_name} parameter '{self.url_key}': {self.value}. "
                    "Expected a single value or a tuple of two values."
                )

            self.is_range_slider = True

    def sync_query_params(self) -> None:
        """Sync select slider value with URL parameter."""

        options_map = {str(v): v for v in self.options}

        if self.is_range_slider:

            str_values = self.validate_multi_url_values(
                self.url_value, min_values=2, max_values=2, allow_none=False
            )

            invalid_values = [v for v in str_values if v not in self.str_options]
            if invalid_values:
                self.raise_url_error(
                    f"Invalid values: {invalid_values}. Expected one of: {self.str_options}"
                )

            actual_values = [options_map[v] for v in str_values]
            start_idx = self.options.index(actual_values[0])
            end_idx = self.options.index(actual_values[1])

            if start_idx > end_idx:
                self.raise_url_error(
                    f"Invalid range for select slider: start value '{actual_values[0]}' comes after end value '{actual_values[1]}' in options."
                )

            self.bound_args.arguments["value"] = actual_values

        else:
            str_value: str = self.validate_single_url_value_disallow_none(
                self.url_value
            )

            if str_value not in self.str_options:
                self.raise_url_error(
                    f"Invalid value: {str_value}. Expected one of: {self.str_options}"
                )

            actual_url_value = options_map[str_value]
            self.bound_args.arguments["value"] = actual_url_value

    @classmethod
    def verify_update_url_value(cls, value: Any) -> Any:
        """Verify that the value is a single value or a tuple of two values."""

        if isinstance(value, (tuple, list)):
            if len(value) != 2:  # type: ignore
                raise ValueError(
                    f"Select slider value must be a single value or a tuple of two values, got {value}."
                )
            return tuple(value)  # type: ignore
        return value

    @classmethod
    def verify_get_url_value(cls, value: Any) -> Any:
        """Verify that the value is a list of one or two strings."""

        return validate_multi_url_values(
            value, min_values=1, max_values=2, allow_none=False
        )
