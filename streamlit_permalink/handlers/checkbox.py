from typing import Any

from ..url_validators import validate_bool, validate_single_url_value

from .handler import WidgetHandler
from ..constants import TRUE_URL_VALUE, FALSE_URL_VALUE


class CheckboxHandler(WidgetHandler):

    def validate_bool(self, value: str) -> bool:
        """
        Validate that the value is a boolean.
        """

        try:
            return validate_bool(value)
        except ValueError as err:
            self.raise_url_error(
                f"Invalid value for checkbox: '{value}'. Expected {TRUE_URL_VALUE} or {FALSE_URL_VALUE}.",
                err=err,
            )

    def sync_query_params(self) -> None:
        str_value: str = self.validate_single_url_value(
            self.url_value, allow_none=False
        )
        bool_value: bool = self.validate_bool(str_value)
        self.bound_args.arguments["value"] = bool_value

    @classmethod
    def verify_update_url_value(cls, value: Any) -> Any:
        if not isinstance(value, bool):
            raise ValueError(
                f"{cls.__name__} value must be a boolean, got {type(value)}"
            )
        return value

    @classmethod
    def verify_get_url_value(cls, value: Any) -> Any:
        return [validate_bool(validate_single_url_value(value, allow_none=False))]
