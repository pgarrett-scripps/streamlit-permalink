from typing import Any, Callable, List, Optional
import inspect

import streamlit as st

from ..exceptions import UrlParamError
from ..utils import (
    init_url_value,
    to_url_value,
)


class HandleWidget:
    """
    Base class for handling Streamlit widgets.
    This class is designed to manage the URL state of Streamlit widgets,
    ensuring that the widget's state is synchronized with the URL parameters.

    Attributes:
        base_widget: The base widget to handle
        url_key: Parameter key in URL
        url_value: Value(s) from URL parameter, None if not present
        bound_args: Bound arguments for the base_widget call
        compressor: Compressor function for url_value
        decompressor: Decompressor function for url_value
        init_url: Boolean indicating whether to initialize URL value
        validate_url: Boolean indicating whether to validate URL value

    returns:
        The widget's return value

    """

    def __init__(
        self,
        base_widget: st.delta_generator.DeltaGenerator,
        url_key: str,
        url_value: Optional[List[str]],
        bound_args: inspect.BoundArguments,
        compressor: Callable,
        decompressor: Callable,
        init_url: bool,
    ):
        self.base_widget = base_widget
        self.url_key = url_key
        self.raw_url_value = url_value
        self.bound_args = bound_args
        self.compressor = compressor
        self.decompressor = decompressor
        self.init_url = init_url

        self.url_value = None
        if self.has_url_value:
            self.url_value = self.decompressor(self.raw_url_value)

    def update_bound_args(self) -> None:
        """
        Parse the URL value and return the parsed value.
        This method should be overridden in subclasses to provide specific parsing logic.
        """
        raise NotImplementedError("Subclasses must implement update_bound_args.")

    def update_url_param(self, value: Any):
        """
        Set the URL value(s) in the query params.
        """
        init_url_value(self.url_key, self.compressor(to_url_value(value)))

    @property
    def has_url_value(self) -> bool:
        """
        Check if the URL value is present in the query params
        """
        return self.raw_url_value is not None

    @property
    def handler_name(self) -> str:
        """
        Get the name of the handler.
        """
        return self.base_widget.__name__

    def url_init(self, widget_value: Any) -> None:
        """
        Initialize the URL value(s) in the query params.
        """
        if self.init_url:
            self.update_url_param(widget_value)

    def run(self) -> Any:

        if not self.has_url_value:
            widget_value = self.base_widget(**self.bound_args.arguments)
            self.url_init(widget_value)
            return widget_value

        self.update_bound_args()

        return self.base_widget(**self.bound_args.arguments)

    def raise_url_error(self, message: str, err=None) -> None:
        """
        Raise an error with the given message.
        """

        if err:
            raise UrlParamError(
                message=message,
                url_key=self.url_key,
                url_value=self.url_value,
                handler=self.handler_name,
            ) from err

        raise UrlParamError(
            message=message,
            url_key=self.url_key,
            url_value=self.url_value,
            handler=self.handler_name,
        )

    def validate_single_url_value(
        self,
        url_value: Optional[List[str]] = None,
        allow_none: bool = False,
    ) -> Optional[str]:
        """
        Validate single value from URL parameter.
        """
        if url_value is None:

            if not allow_none:
                self.raise_url_error("None value is not allowed.")

            return None

        if not (isinstance(url_value, (list, tuple)) and len(url_value) == 1):
            self.raise_url_error("Expected a single value, but got multiple values.")

        return self.url_value[0]

    def validate_multi_url_values(
        self,
        url_values: Optional[List[str]] = None,
        min_values: Optional[int] = None,
        max_values: Optional[int] = None,
        allow_none: bool = False,
    ) -> List[str]:
        """
        Validate that all multiselect values are in the options list.
        """
        # Handle special case for empty selection
        if url_values is None:

            if not allow_none:
                self.raise_url_error("None value is not allowed.")

            return []

        if not isinstance(url_values, (list, tuple)):
            self.raise_url_error("Expected a list of values.")

        if min_values != None and len(url_values) < min_values:
            self.raise_url_error(
                f"Expected at least {min_values} values, but got {len(url_values)}."
            )

        if max_values != None and len(url_values) > max_values:
            self.raise_url_error(
                f"Expected at most {max_values} values, but got {len(url_values)}."
            )

        return url_values
