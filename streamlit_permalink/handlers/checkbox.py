"""
Handle checkbox widget URL state synchronization.
"""

from typing import Callable, List, Optional
import inspect

import streamlit as st

from ..utils import (
    init_url_value,
    to_url_value,
    validate_bool_url_value,
    validate_single_url_value,
)

_HANDLER_NAME = "checkbox"
_DEFAULT_VALUE = False


def handle_checkbox(
    base_widget: st.delta_generator.DeltaGenerator,
    url_key: str,
    url_value: Optional[List[str]],
    bound_args: inspect.BoundArguments,
    compressor: Callable,
    decompressor: Callable,
) -> bool:
    """
    Handle checkbox widget URL state synchronization.

    Args:
        base_widget: The base widget to handle
        url_key: Parameter key in URL
        url_value: Value(s) from URL parameter, None if not present
        bound_args: Bound arguments for the base_widget call
        compressor: Compressor function for url_value
        decompressor: Decompressor function for url_value

    Returns:
        Boolean state of the checkbox widget

    Raises:
        UrlParamError: If URL value is invalid
    """
    # Initialize from default when no URL value exists
    if url_value is None:
        default_value = bound_args.arguments.get("value", _DEFAULT_VALUE)
        init_url_value(url_key, compressor(to_url_value(default_value)))
        return base_widget(**bound_args.arguments)

    url_value = decompressor(url_value)  # [str, str], [], None

    # Process URL value: ensure single value and convert to boolean
    validated_value = validate_single_url_value(url_key, url_value, _HANDLER_NAME)
    url_value_bool = validate_bool_url_value(url_key, validated_value, _HANDLER_NAME)

    # Update widget state with URL value
    bound_args.arguments["value"] = url_value_bool
    return base_widget(**bound_args.arguments)
