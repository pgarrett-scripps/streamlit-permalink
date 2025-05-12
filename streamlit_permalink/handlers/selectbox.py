from typing import Optional

from .handler import WidgetHandler
from ..utils import (
    _validate_multi_options,
)


class SelectboxHandler(WidgetHandler):

    def __init__(self, *args, **kwargs):
        """
        Initialize the HandlerSelectbox instance.
        """
        super().__init__(*args, **kwargs)
        self.options = self.bound_args.arguments.get("options")
        self.str_options = _validate_multi_options(self.options, self.handler_name)

        self.accept_new_options = self.bound_args.arguments.get(
            "accept_new_options", False
        )

    def sync_query_params(self) -> None:
        str_value: Optional[str] = self.validate_single_url_value(
            self.url_value, allow_none=True
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
