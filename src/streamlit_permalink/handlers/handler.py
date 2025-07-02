import inspect
from functools import partial
from typing import Any, Callable, List, Optional

import streamlit as st
from packaging.version import parse as V
from streamlit.delta_generator import DeltaGenerator

from ..exceptions import UrlParamError
from ..url_validators import (
    validate_multi_url_values,
    validate_single_url_value_allow_none,
    validate_single_url_value_disallow_none,
)
from ..utils import (
    DEFAULT_COMPRESSOR,
    DEFAULT_DECOMPRESSOR,
    compress_list,
    decompress_list,
    init_url_value,
    to_url_value,
)


class WidgetHandler:
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
        base_widget: DeltaGenerator,
        url_key: str,
        url_value: Optional[List[str]],
        bound_args: inspect.BoundArguments,
        compressor: Callable[..., str],
        decompressor: Callable[..., Any],
        init_url: bool,
    ) -> None:
        self.base_widget = base_widget
        self.url_key = url_key
        self.raw_url_value = url_value
        self.bound_args = bound_args
        self.compressor = compressor
        self.decompressor = decompressor
        self.init_url = init_url

        self.url_value: Optional[List[str]] = None
        if self.has_url_value:
            self.url_value = self.decompressor(self.raw_url_value)

    def sync_query_params(self) -> None:
        """
        Parse the URL value and return the parsed value.

        This method should be overridden in subclasses to provide specific parsing logic.
        """

        raise NotImplementedError("Subclasses must implement update_bound_args.")

    def update_url_param(self, value: Any):
        """Set the URL value(s) in the query params."""

        init_url_value(self.url_key, self.compressor(to_url_value(value)))

    @property
    def has_url_value(self) -> bool:
        """Check if the URL value is present in the query params."""

        return self.raw_url_value is not None

    @property
    def handler_name(self) -> str:
        """Get the name of the handler."""

        return self.base_widget.__name__  # type: ignore

    def url_init(self, widget_value: Any) -> None:
        """Initialize the URL value(s) in the query params."""

        if self.init_url:
            self.update_url_param(widget_value)

    def run(self) -> Any:

        if not self.has_url_value:
            widget_value = self.base_widget(**self.bound_args.arguments)  # type: ignore
            self.url_init(widget_value)
            return widget_value  # type: ignore

        self.sync_query_params()

        return self.base_widget(**self.bound_args.arguments)  # type: ignore

    def raise_url_error(self, message: str, err: Optional[Exception] = None) -> None:
        """Raise an error with the given message."""

        if err:
            raise UrlParamError(
                message=message,
                url_key=self.url_key,
                url_value=self.url_value,
                handler_name=self.handler_name,
            ) from err

        raise UrlParamError(
            message=message,
            url_key=self.url_key,
            url_value=self.url_value,
            handler_name=self.handler_name,
        )

    def validate_single_url_value_allow_none(
        self,
        url_value: Optional[List[str]] = None,
    ) -> Optional[str]:
        return validate_single_url_value_allow_none(url_value)

    def validate_single_url_value_disallow_none(
        self,
        url_value: Optional[List[str]] = None,
    ) -> str:
        return validate_single_url_value_disallow_none(url_value)

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
        try:
            return validate_multi_url_values(
                url_values,
                min_values=min_values,
                max_values=max_values,
                allow_none=allow_none,
            )
        except ValueError as err:
            self.raise_url_error(
                f"Invalid values for {self.handler_name}: {err}",
                err=err,
            )

        raise RuntimeError("Unreachable code")

    @classmethod
    def verify_update_url_value(cls, value: Any) -> Any:
        # Override this method to verify the value before updating the URL.
        raise NotImplementedError(
            f"{cls.__name__} must implement verify_update_url_value method."
        )

    @classmethod
    def update_url(
        cls,
        value: Any,
        url_key: str,
        compressor: Optional[Callable[..., str]] = None,
        compress: bool = False,
    ) -> None:
        """
        Update the URL parameter
        """

        if compressor is None and compress is True:
            compressor = DEFAULT_COMPRESSOR  # type: ignore

        if compress is False:
            compressor = partial(compress_list, lambda x: x)  # type: ignore

        value = cls.verify_update_url_value(value)

        init_url_value(url_key, compressor(to_url_value(value)))  # type: ignore

    @classmethod
    def verify_get_url_value(cls, value: Any) -> Any:
        # Override this method to verify the value before updating the URL.
        raise NotImplementedError(
            f"{cls.__name__} must implement verify_get_url_value method."
        )

    @classmethod
    def get_url_value(
        cls,
        url_key: str,
        decompressor: Optional[Callable[..., List[str]]] = None,
        compress: bool = False,
    ) -> Any:
        """
        Get the URL value for the given key.
        """
        if decompressor is None and compress is True:
            decompressor = DEFAULT_DECOMPRESSOR  # type: ignore
        if compress is False:
            decompressor = partial(decompress_list, lambda x: x)  # type: ignore

        if V(st.__version__) < V("1.30"):
            raw_url_value = st.experimental_get_query_params().get(url_key, None)
        else:
            raw_url_value = st.query_params.get_all(url_key)
            if len(raw_url_value) == 0:
                raw_url_value = None

        if raw_url_value is None:
            return None

        return cls.verify_get_url_value(decompressor(raw_url_value))  # type: ignore
