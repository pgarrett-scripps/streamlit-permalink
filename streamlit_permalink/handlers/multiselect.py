from typing import Any, Iterable, List

from ..url_validators import validate_multi_url_values

from .handler import WidgetHandler
from ..utils import (
    _validate_multi_options,
)


class MultiSelectHandler(WidgetHandler):

    def __init__(self, *args, **kwargs):
        """
        Initialize the HandlerMultiSelect instance.
        """
        super().__init__(*args, **kwargs)
        self.options = self.bound_args.arguments.get("options")
        self.str_options: List[str] = _validate_multi_options(
            self.options, self.handler_name
        )

        self.accept_new_options = self.bound_args.arguments.get(
            "accept_new_options", False
        )

    def sync_query_params(self) -> None:
        str_values = self.validate_multi_url_values(
            self.url_value, min_values=None, max_values=None, allow_none=True
        )

        # Validate all values are in options
        invalid_str_values = [v for v in str_values if v not in self.str_options]

        if self.accept_new_options:
            self.options.extend(invalid_str_values)
            self.bound_args.arguments["options"] = self.options
        else:
            if invalid_str_values:
                self.raise_url_error(f"Invalid values: {invalid_str_values}")

        # Convert string values back to original option values
        options_map = {str(v): v for v in self.options}
        actual_values = [options_map[v] for v in str_values]
        self.bound_args.arguments["default"] = actual_values

    @classmethod
    def verify_update_url_value(cls, value: Any) -> Any:
        if not isinstance(value, Iterable):
            raise ValueError(f"MultiSelect value must be a list, got {type(value)}")
        return value

    @classmethod
    def verify_get_url_value(cls, value: Any) -> Any:
        return validate_multi_url_values(value, allow_none=False)
