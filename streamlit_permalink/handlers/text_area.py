from .handler import WidgetHandler


class TextAreaHandler(WidgetHandler):
    """
    Handler for text area widget URL state synchronization.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.max_chars = self.bound_args.arguments.get("max_chars", None)

    def update_bound_args(self) -> None:

        # Get the validated single URL value
        value = self.validate_single_url_value(self.url_value, allow_none=True)

        if value is None:
            # If no URL value is provided, set value to None
            self.bound_args.arguments["value"] = None
            return

        # Check if the value exceeds the maximum characters limit
        if self.max_chars is not None and len(value) > self.max_chars:
            self.raise_url_error(
                f"Text exceeds maximum allowed characters: {len(value)} " \
                f"characters provided, but limit is {self.max_chars}"
            )

        # Update bound arguments with validated value
        self.bound_args.arguments["value"] = value
