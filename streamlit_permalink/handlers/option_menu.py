from typing import Any

from ..url_validators import validate_single_url_value
from .handler import WidgetHandler
from ..utils import (
    _validate_multi_options,
)


class OptionMenuHandler(WidgetHandler):

    def __init__(self, *args, **kwargs):
        """
        Initialize the HandlerOptionMenu instance.
        """
        super().__init__(*args, **kwargs)
        self.options = self.bound_args.arguments.get("options")
        self.str_options = _validate_multi_options(self.options, self.handler_name)

    def sync_query_params(self) -> None:
        str_value = self.validate_single_url_value(self.url_value, allow_none=False)
        options_map = {str(v): v for v in self.options}

        if str_value not in options_map:
            self.raise_url_error(
                f"Invalid value for option menu: '{str_value}'. Expected one of: {self.str_options}"
            )

        actual_value = options_map[str_value]
        self.bound_args.arguments["default_index"] = self.options.index(actual_value)

    @classmethod
    def verify_update_url_value(cls, value: Any) -> Any:
        if not isinstance(value, str):
            raise ValueError(f"OptionMenu value must be a string, got {type(value)}")
        return value

    @classmethod
    def verify_get_url_value(cls, value: Any) -> Any:
        return [validate_single_url_value(value, allow_none=False)]
