from typing import Any, Optional, Union

from ..url_validators import validate_single_url_value_allow_none
from .handler import WidgetHandler


class NumberInputHandler(WidgetHandler):

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Initialize the NumberInputHandler instance."""

        super().__init__(*args, **kwargs)
        self.value = self.bound_args.arguments.get("value", "min")
        if self.value == "min":
            self.value = self.bound_args.arguments.get("min_value", 0.0)

        self.value_type: type = type(self.value)

        # Validate input value type
        if self.value_type not in (int, float, type(None)):
            self.raise_url_error("Expected int, float or None value.")

        self.min_value: Optional[float] = self.bound_args.arguments.get(
            "min_value", None
        )
        self.max_value: Optional[float] = self.bound_args.arguments.get(
            "max_value", None
        )

    def validate_bounds(self, value: Union[int, float]) -> None:
        """Validate the bounds of the number input."""

        if self.min_value is not None and value < self.min_value:
            self.raise_url_error(
                f"Value {value} is less than the minimum allowed value {self.min_value}."
            )
        if self.max_value is not None and value > self.max_value:
            self.raise_url_error(
                f"Value {value} is greater than the maximum allowed value {self.max_value}."
            )

    def sync_query_params(self) -> None:
        """Sync number input value with URL parameter."""

        str_value = self.validate_single_url_value_allow_none(self.url_value)

        if str_value is None:

            if self.value_type != type(None):
                self.raise_url_error("None value is not allowed.")

            self.bound_args.arguments["value"] = None
            return

        parsed_value = None
        try:
            if self.value_type == int:
                parsed_value = int(str_value)
            elif self.value_type == float:
                parsed_value = float(str_value)
            elif self.value_type == type(None):
                # For None type, try float first, then int if that fails, or keep as None
                try:
                    parsed_value = int(str_value)
                except (ValueError, TypeError):
                    parsed_value = float(str_value)
        except (ValueError, TypeError) as err:
            type_name = (
                "int"
                if self.value_type == int
                else "float" if self.value_type == float else "int, float"
            )
            self.raise_url_error(f"Expected {type_name} value.", err)
            raise RuntimeError("Unreachable")

        if parsed_value is None:
            self.raise_url_error("Failed to parse value.")
            raise RuntimeError("Unreachable")

        self.validate_bounds(parsed_value)
        self.bound_args.arguments["value"] = parsed_value

    @classmethod
    def verify_update_url_value(cls, value: Any) -> Any:
        """Verify the value to be updated in the URL."""

        if not isinstance(value, (int, float, type(None))):
            raise ValueError(f"Value must be int, float or None, got {type(value)}")
        return value

    @classmethod
    def verify_get_url_value(cls, value: Any) -> Any:
        """Verify the value to be set in the URL."""

        str_value = validate_single_url_value_allow_none(value)

        if str_value is None:
            return [None]

        try:
            return [int(str_value)]
        except ValueError:
            try:
                return [float(str_value)]
            except ValueError:
                raise ValueError(
                    f"Invalid number format: {str_value}. Expected int or float."
                )
