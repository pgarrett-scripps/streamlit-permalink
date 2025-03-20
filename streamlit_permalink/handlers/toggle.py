"""
Handle toggle widget URL state synchronization.
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

_DEFAULT_VALUE = False
_HANDLER_NAME = "toggle"


def handle_toggle(
    base_widget: st.delta_generator.DeltaGenerator,
    url_key: str,
    url_value: Optional[List[str]],
    bound_args: inspect.BoundArguments,
    compressor: Callable,
    decompressor: Callable,
) -> bool:
    """
    Handle toggle widget URL state synchronization.

    Args:
        base_widget: The base widget to handle
        url_key: Parameter key in URL
        url_value: Value(s) from URL parameter, None if not present
        bound_args: Bound arguments for the base_widget call
        compressor: Compressor function for url_value
        decompressor: Decompressor function for url_value

    Returns:
        bool: The toggle widget's return value (True if toggled on, False otherwise)
    """
    # Handle the default case when no URL value is provided
    if url_value is None:
        default_value = bound_args.arguments.get("value", _DEFAULT_VALUE)
        init_url_value(url_key, compressor(to_url_value(default_value)))
        return base_widget(**bound_args.arguments)

    url_value = decompressor(url_value)

    # Process and validate the URL value
    url_value_str = validate_single_url_value(url_key, url_value, _HANDLER_NAME)
    url_value_bool = validate_bool_url_value(url_key, url_value_str, _HANDLER_NAME)

    # Update the bound arguments with the validated value
    bound_args.arguments["value"] = url_value_bool
    return base_widget(**bound_args.arguments)
