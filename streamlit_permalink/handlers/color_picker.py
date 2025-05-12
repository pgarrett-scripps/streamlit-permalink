import re
from .handler import WidgetHandler


class ColorPickerHandler(WidgetHandler):

    def validate_color(self, value: str) -> str:
        """
        Validate that the value is a valid color.
        """
        if not re.match(r"^#([0-9a-fA-F]{6})$", value):
            self.raise_url_error(
                f"Invalid color format: {value}. Expected format: #RRGGBB."
            )

        return value

    def sync_query_params(self) -> None:

        str_value: str = self.validate_single_url_value(
            self.url_value, allow_none=False
        )
        color_value: str = self.validate_color(str_value)
        self.bound_args.arguments["value"] = color_value
