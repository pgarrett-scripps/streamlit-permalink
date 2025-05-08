import re
from .handler import HandleWidget


class HandlerColorPicker(HandleWidget):

    def update_bound_args(self) -> None:
        
        str_value = self.validate_single_url_value(allow_none=False)

        if not re.match(r"^#([0-9a-fA-F]{6})$", str_value):
            self.raise_url_error(f"Invalid color format. Expected format: #RRGGBB.")
        
        self.bound_args.arguments["value"] = str_value
