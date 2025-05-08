from .handler import HandleWidget
from ..utils import (
    _validate_multi_options,
    validate_single_url_value,
)
from ..exceptions import UrlParamError


class HandlerOptionMenu(HandleWidget):

    def __init__(self, *args, **kwargs):
        """
        Initialize the HandlerOptionMenu instance.
        """
        super().__init__(*args, **kwargs)
        self.options = self.bound_args.arguments.get("options")
        self.str_options = _validate_multi_options(self.options, self.handler_name)

    def update_bound_args(self) -> None:
        str_value = self.validate_single_url_value(allow_none=False)
        options_map = {str(v): v for v in self.options}

        if str_value not in options_map:
            self.raise_url_error(
                f"Invalid value for option menu: '{str_value}'. Expected one of: {self.str_options}"
            )

        actual_value = options_map[str_value]
        self.bound_args.arguments["default_value"] = actual_value