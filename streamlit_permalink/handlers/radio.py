from typing import Optional

from .handler import HandleWidget
from ..utils import (
    _validate_multi_options,
    validate_single_url_value,
)
from ..exceptions import UrlParamError


class HandlerRadio(HandleWidget):

    def __init__(self, *args, **kwargs):
        """
        Initialize the HandlerRadio instance.
        """
        super().__init__(*args, **kwargs)
        self.options = self.bound_args.arguments.get("options")
        self.str_options = _validate_multi_options(self.options, self.handler_name)


    def update_bound_args(self) -> None:

        str_value: Optional[str] = self.validate_single_url_value(allow_none=True)

        if str_value is None:
            self.bound_args.arguments["index"] = None
            return

        options_map = {str(v): v for v in self.options}

        if str_value not in options_map:
            self.raise_url_error(
                f"Invalid value for radio button: '{str_value}'. Expected one of: {self.str_options}"
            )

        actual_url_value = options_map[str_value]
        self.bound_args.arguments["index"] = self.options.index(actual_url_value)
