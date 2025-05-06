"""
Handle multiselect widget URL state synchronization.
"""

from typing import Any, Callable, List, Optional
import inspect

import streamlit as st

from ..exceptions import UrlParamError

from ..utils import (
    _validate_multi_default,
    _validate_multi_options,
    init_url_value,
    to_url_value,
)

_HANDLER_NAME = "multiselect"
_DEFAULT_VALUE = None


def handle_multiselect(
    base_widget: st.delta_generator.DeltaGenerator,
    url_key: str,
    url_value: Optional[List[str]],
    bound_args: inspect.BoundArguments,
    compressor: Callable,
    decompressor: Callable,
) -> Any:
    """
    Handle multiselect widget URL state synchronization.

    Args:
        base_widget: The base widget to handle
        url_key: Parameter key in URL
        url_value: Value(s) from URL parameter, None if not present
        bound_args: Bound arguments for the base_widget call
        compressor: Compressor function for url_value
        decompressor: Decompressor function for url_value

    Returns:
        The multiselect widget's return value (list of selected options)

    Raises:
        ValueError: If options are invalid
        UrlParamError: If URL values are invalid
    """
    # Get and validate options
    options = bound_args.arguments.get("options")
    str_options: List[str] = _validate_multi_options(options, _HANDLER_NAME)

    # Get and validate default values
    default = bound_args.arguments.get("default", _DEFAULT_VALUE)
    _ = _validate_multi_default(default, options, _HANDLER_NAME)

    # If no URL value is provided, initialize with default value
    if url_value is None:
        init_url_value(url_key, compressor(to_url_value(default)))
        return base_widget(**bound_args.arguments)

    url_values = decompressor(url_value)

    # Handle special case for empty selection
    if url_values is None:
        return []

    # Validate all values are in options
    invalid_values = [v for v in url_values if v not in str_options]

    if bound_args.arguments.get("accept_new_options", False):
        # add invalid values to options
        options.extend(invalid_values)
        bound_args.arguments["options"] = options
    else:
        if invalid_values:
            raise UrlParamError(
                f"Invalid {_HANDLER_NAME.capitalize()} selection for '{url_key}': {invalid_values}. "
                f"Valid options are: {str_options}"
            )

    # Convert string values back to original option values
    options_map = {str(v): v for v in options}
    actual_url_values = [options_map[v] for v in url_values]

    # Update bound arguments with validated values
    bound_args.arguments["default"] = actual_url_values
    return base_widget(**bound_args.arguments)
