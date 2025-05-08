from types import NoneType
from typing import Any

from .handler import HandleWidget
from ..exceptions import UrlParamError
from ..utils import validate_single_url_value

class HandlerNumberInput(HandleWidget):

    def __init__(self, *args, **kwargs):
        """
        Initialize the HandlerMultiSelect instance.
        """
        super().__init__(*args, **kwargs)
        self.value = self.bound_args.arguments.get("value", "min")
        if self.value == "min":
            self.value = self.bound_args.arguments.get("min_value", 0.0)

        self.value_type = type(self.value)

        # Validate input value type
        if self.value_type not in (int, float, NoneType):
            self.raise_url_error("Expected int, float or None value.")

        self.min_value = self.bound_args.arguments.get("min_value", None)
        self.max_value = self.bound_args.arguments.get("max_value", None)

    def validate_bounds(self, value: Any) -> None:
        """
        Validate the bounds of the number input.
        """
        if self.min_value is not None and value < self.min_value:
            self.raise_url_error(
                f"Value {value} is less than the minimum allowed value {self.min_value}."
            )
        if self.max_value is not None and value > self.max_value:
            self.raise_url_error(
                f"Value {value} is greater than the maximum allowed value {self.max_value}."
            )

    def update_bound_args(self) -> None:

        # Parse the URL value
        str_value = self.validate_single_url_value(allow_none=True)

        if str_value is None:

            if self.value_type != NoneType:
                self.raise_url_error("None value is not allowed.")

            self.bound_args.arguments["value"] = None
            return

        try:
            if self.value_type == int:
                parsed_value = int(str_value)
            elif self.value_type == float:
                parsed_value = float(str_value)
            elif self.value_type == NoneType:
                # For None type, try float first, then int if that fails, or keep as None
                try:
                    parsed_value = int(str_value)
                except (ValueError, TypeError):
                    parsed_value = float(str_value)
        except (ValueError, TypeError) as err:
            type_name = "int" if self.value_type == int else "float" if self.value_type == float else "int, float"
            self.raise_url_error(f"Expected {type_name} value.", err)

        # Validate the parsed value against min and max bounds
        self.validate_bounds(parsed_value)

        self.bound_args.arguments["value"] = parsed_value
        