from typing import Any, Iterable, List

from ..url_validators import validate_multi_url_values

from .handler import WidgetHandler

from ..utils import (
    _validate_selection_mode,
    _validate_multi_options,
)


class PillsHandler(WidgetHandler):

    def __init__(self, *args, **kwargs):
        """
        Initialize the HandlerPills instance.
        """
        super().__init__(*args, **kwargs)
        self.options = self.bound_args.arguments.get("options", None)
        self.str_options: List[str] = _validate_multi_options(
            self.options, self.handler_name
        )

        self.selection_mode = _validate_selection_mode(
            self.bound_args.arguments.get("selection_mode", "single")
        )

    def sync_query_params(self) -> None:

        # Validate URL values against options
        str_values: List[str] = self.validate_multi_url_values(
            self.url_value, min_values=None, max_values=None, allow_none=True
        )

        if self.selection_mode == "single" and len(str_values) > 1:
            self.raise_url_error("Multiple values provided for single selection mode.")

        # Validate all values are in options
        invalid_str_values = [v for v in str_values if v not in self.str_options]

        if len(invalid_str_values) > 0:
            self.raise_url_error(
                f"Invalid values: {invalid_str_values}. Expected one of: {self.str_options}"
            )

        # Convert string values back to original option values
        options_map = {str(v): v for v in self.options}
        actual_values = [options_map[v] for v in str_values]
        self.bound_args.arguments["default"] = actual_values

    @classmethod
    def verify_update_url_value(cls, value: Any) -> Any:
        if not isinstance(value, Iterable):
            raise ValueError(f"Pills value must be a list, got {type(value)}")
        return value

    @classmethod
    def verify_get_url_value(cls, value: Any) -> Any:
        return validate_multi_url_values(
            value, min_values=None, max_values=None, allow_none=True
        )
