"""Handler for checkbox widget URL state synchronization."""

from typing import Any

from ..constants import FALSE_URL_VALUE, TRUE_URL_VALUE
from ..url_validators import validate_bool, validate_single_url_value_disallow_none
from .handler import WidgetHandler


class CheckboxHandler(WidgetHandler):
    """Handler for checkbox widget URL state synchronization."""

    def validate_bool(self, value: str) -> bool:
        """Validate that the value is a boolean."""

        try:
            return validate_bool(value)
        except ValueError as err:
            self.raise_url_error(
                f"Invalid value for checkbox: '{value}'. Expected {TRUE_URL_VALUE} or {FALSE_URL_VALUE}.",
                err=err,
            )

        raise RuntimeError("Unreachable")

    def sync_query_params(self) -> None:
        """Sync checkbox value with URL parameter."""

        str_value = self.validate_single_url_value_disallow_none(self.url_value)
        bool_value = self.validate_bool(str_value)
        self.bound_args.arguments["value"] = bool_value

    @classmethod
    def verify_update_url_value(cls, value: Any) -> Any:
        """Verify that the value is a boolean."""

        if not isinstance(value, bool):
            raise ValueError(
                f"{cls.__name__} value must be a boolean, got {type(value)}"
            )
        return value

    @classmethod
    def verify_get_url_value(cls, value: Any) -> Any:
        """Validate the URL value for checkbox."""

        return [validate_bool(validate_single_url_value_disallow_none(value))]
