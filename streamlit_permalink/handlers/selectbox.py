"""
Handle selectbox widget URL state synchronization.
"""

from typing import Callable, List, Optional
import inspect

import streamlit as st

from ..utils import (
    _validate_multi_options,
    init_url_value,
    to_url_value,
    validate_single_url_value,
)
from ..exceptions import UrlParamError

_HANDLER_NAME = "selectbox"


def handle_selectbox(
    base_widget: st.delta_generator.DeltaGenerator,
    url_key: str,
    url_value: Optional[List[str]],
    bound_args: inspect.BoundArguments,
    compressor: Callable,
    decompressor: Callable,
):
    """
    Handle selectbox widget URL state.

    Args:
        base_widget: The base widget to handle
        url_key: Parameter key in URL
        url_value: Value(s) from URL parameter, None if not present
        bound_args: Bound arguments for the base_widget call
        compressor: Compressor function for url_value
        decompressor: Decompressor function for url_value

    Returns:
        The selectbox widget's return value

    Raises:
        UrlParamError: If URL value is invalid
    """

    options = bound_args.arguments.get("options")
    _ = _validate_multi_options(options, _HANDLER_NAME)

    index = bound_args.arguments.get("index", 0)
    bound_args.arguments["index"] = index

    value = options[index]

    if not url_value:
        init_url_value(url_key, compressor(to_url_value(value)))
        return base_widget(**bound_args.arguments)

    url_value = decompressor(url_value)

    url_value: Optional[str] = validate_single_url_value(
        url_key, url_value, _HANDLER_NAME
    )

    if url_value is not None:
        try:
            options_map = {str(v): v for v in options}
            actual_url_value = options_map[url_value]
            bound_args.arguments["index"] = options.index(actual_url_value)
        except KeyError as err:
            if bound_args.arguments.get("accept_new_options", False):
                bound_args.arguments.get("options").append(url_value)
                bound_args.arguments["index"] = bound_args.arguments.get(
                    "options"
                ).index(url_value)
                return base_widget(**bound_args.arguments)

            raise UrlParamError(
                f"Invalid value for {_HANDLER_NAME} parameter '{url_key}': {url_value}. "
                f"Expected one of {options}."
            ) from err
    else:
        bound_args.arguments["index"] = None

    return base_widget(**bound_args.arguments)
