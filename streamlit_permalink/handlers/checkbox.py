from .handler import WidgetHandler


class CheckboxHandler(WidgetHandler):

    def validate_bool(self, value: str) -> bool:
        """
        Validate that the value is a boolean.
        """
        value = value.capitalize()
        if value not in ["True", "False"]:
            self.raise_url_error(
                f"Invalid value for checkbox: '{value}'. Expected 'True' or 'False'."
            )

        return value == "True"

    def update_bound_args(self) -> None:

        str_value: str = self.validate_single_url_value(
            self.url_value, allow_none=False
        ).capitalize()
        bool_value: bool = self.validate_bool(str_value)
        self.bound_args.arguments["value"] = bool_value
