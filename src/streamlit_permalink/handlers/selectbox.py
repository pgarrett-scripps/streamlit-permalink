from typing import Any, List, Optional

from ..url_validators import validate_single_url_value_allow_none
from ..utils import (
    validate_multi_options,
)
from .handler import WidgetHandler


class SelectboxHandler(WidgetHandler):

    def __init__(self, *args: Any, **kwargs: Any):
        """Initialize the HandlerSelectbox instance."""

        super().__init__(*args, **kwargs)
        options = self.bound_args.arguments.get("options")

        self.options: List[Any]
        if options is None:
            self.options = []
        else:
            self.options = options

        self.str_options = validate_multi_options(self.options, self.handler_name)

        self.accept_new_options = self.bound_args.arguments.get(
            "accept_new_options", False
        )

    def sync_query_params(self) -> None:
        """Sync selectbox value with URL parameter."""

        str_value: Optional[str] = self.validate_single_url_value_allow_none(
            self.url_value
        )

        if str_value is None:
            self.bound_args.arguments["index"] = None
            return

        if str_value not in self.str_options:

            if not self.accept_new_options:
                self.raise_url_error(
                    f"Invalid value for selectbox: '{str_value}'. Expected one of: {self.str_options}"
                )

            self.options.append(str_value)
            self.str_options.append(str_value)

        options_map = {str(v): v for v in self.options}
        actual_value = options_map[str_value]
        self.bound_args.arguments["index"] = self.options.index(actual_value)

    @classmethod
    def verify_update_url_value(cls, value: Any) -> Any:
        """Verify that the value is a string or None."""

        return value

    @classmethod
    def verify_get_url_value(cls, value: Any) -> Any:
        """Verify that the value is a list of strings or None."""

        return [validate_single_url_value_allow_none(value)]
