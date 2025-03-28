"""
Handle text input widget URL state synchronization.
"""

from typing import Callable, List, Optional
import inspect

import streamlit as st

from ..utils import init_url_value, to_url_value, validate_single_url_value
from ..exceptions import UrlParamError

_HANDLER_NAME = "text_input"


def handle_text_input(
    base_widget: st.delta_generator.DeltaGenerator,
    url_key: str,
    url_value: Optional[List[str]],
    bound_args: inspect.BoundArguments,
    compressor: Callable,
    decompressor: Callable,
) -> str:
    """
    Handle text input widget URL state synchronization.

    Args:
        base_widget: The base widget to handle
        url_key: Parameter key in URL
        url_value: Value(s) from URL parameter, None if not present
        bound_args: Bound arguments for the base_widget call
        compressor: Compressor function for url_value
        decompressor: Decompressor function for url_value

    Returns:
        The text input widget's return value (string content)

    Raises:
        UrlParamError: If URL value exceeds maximum allowed characters
    """
    if url_value is None:
        value = bound_args.arguments.get("value", None)
        init_url_value(url_key, compressor(to_url_value(value)))
        return base_widget(**bound_args.arguments)

    url_value = decompressor(url_value)
    url_value = validate_single_url_value(url_key, url_value, _HANDLER_NAME)

    max_chars = bound_args.arguments.get("max_chars")

    if max_chars is not None and len(url_value) > max_chars:
        raise UrlParamError(
            f"Invalid value for {_HANDLER_NAME} parameter '{url_key}': "
            f"length ({len(url_value)}) exceeds maximum allowed characters ({max_chars})."
        )

    bound_args.arguments["value"] = url_value
    return base_widget(**bound_args.arguments)
