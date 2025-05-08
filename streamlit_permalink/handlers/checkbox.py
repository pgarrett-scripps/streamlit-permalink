from .handler import HandleWidget

class HandlerCheckbox(HandleWidget):

    def update_bound_args(self) -> None:

        str_value = self.validate_single_url_value(allow_none=False).capitalize()
        
        if str_value not in ["True", "False"]:
            self.raise_url_error(
                f"Invalid value for checkbox: '{str_value}'. Expected 'True' or 'False'."
            )

        self.bound_args.arguments["value"] = str_value == "True"
