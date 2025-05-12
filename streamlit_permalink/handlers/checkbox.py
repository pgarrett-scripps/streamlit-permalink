from .handler import WidgetHandler
from ..constants import TRUE_URL_VALUE, FALSE_URL_VALUE


class CheckboxHandler(WidgetHandler):

    def validate_bool(self, value: str) -> bool:
        """
        Validate that the value is a boolean.
        """
        value = value.capitalize()
        if value not in [TRUE_URL_VALUE, FALSE_URL_VALUE]:
            self.raise_url_error(
                f"Invalid value for checkbox: '{value}'. Expected {TRUE_URL_VALUE} or {FALSE_URL_VALUE}."
            )

        return value == TRUE_URL_VALUE

    def sync_query_params(self) -> None:

        str_value: str = self.validate_single_url_value(self.url_value, allow_none=False)
        bool_value: bool = self.validate_bool(str_value)
        self.bound_args.arguments["value"] = bool_value
