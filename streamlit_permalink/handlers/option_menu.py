"""
Handle option menu widget URL state synchronization.
"""

from typing import Any, Callable, List, Optional
import inspect

import streamlit as st

from ..utils import (
    _validate_multi_options,
    init_url_value,
    to_url_value,
    validate_single_url_value,
)
from ..exceptions import UrlParamError


_HANDLER_NAME = "option_menu"
_DEFAULT_VALUE = 0


def handle_option_menu(
    base_widget: st.delta_generator.DeltaGenerator,
    url_key: str,
    url_value: Optional[List[str]],
    bound_args: inspect.BoundArguments,
    compressor: Callable,
    decompressor: Callable,
) -> Any:
    """
    Handle option menu widget URL state synchronization.

    Args:
        base_widget: The base widget to handle
        url_key: Parameter key in URL
        url_value: Value(s) from URL parameter, None if not present
        bound_args: Bound arguments for the base_widget call
        compressor: Compressor function for url_value
        decompressor: Decompressor function for url_value

    Returns:
        The option menu widget's return value (selected option)

    Raises:
        UrlParamError: If URL value is invalid or not in the options list
        ValueError: If options are invalid
    """
    options = bound_args.arguments.get("options")
    _ = _validate_multi_options(options, _HANDLER_NAME)

    index = bound_args.arguments.get("default_index", _DEFAULT_VALUE)
    bound_args.arguments["default_index"] = index

    value = options[index]

    if not url_value:
        init_url_value(url_key, compressor(to_url_value(value)))
        return base_widget(**bound_args.arguments)

    url_value = decompressor(url_value)

    url_value_str: Optional[str] = validate_single_url_value(
        url_key, url_value, _HANDLER_NAME
    )

    if url_value_str is None:
        raise UrlParamError(
            f"Invalid value for {_HANDLER_NAME} parameter '{url_key}': {url_value}. Expected a single value."
        )

    try:
        options_map = {str(v): v for v in options}
        actual_url_value = options_map[url_value_str]
        bound_args.arguments["default_index"] = options.index(actual_url_value)
    except KeyError as err:
        raise UrlParamError(
            f"Invalid value for {_HANDLER_NAME} parameter '{url_key}': {url_value_str}. "
            f"Expected one of {options}."
        ) from err

    return base_widget(**bound_args.arguments)
