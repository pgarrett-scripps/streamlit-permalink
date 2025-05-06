"""
Handle number input widget URL state synchronization.
"""

from typing import Callable, List, Optional, Union, Type
import inspect

import streamlit as st

from ..utils import init_url_value, to_url_value, validate_single_url_value
from ..exceptions import UrlParamError

_HANDLER_NAME = "number_input"
_DEFAULT_VALUE = "min"


def handle_number_input(
    base_widget: st.delta_generator.DeltaGenerator,
    url_key: str,
    url_value: Optional[List[str]],
    bound_args: inspect.BoundArguments,
    compressor: Callable,
    decompressor: Callable,
) -> Union[int, float]:
    """
    Handle number input widget URL state synchronization.

    Args:
        base_widget: The base widget to handle
        url_key: Parameter key in URL
        url_value: Value(s) from URL parameter, None if not present
        bound_args: Bound arguments for the base_widget call
        compressor: Compressor function for url_value
        decompressor: Decompressor function for url_value

    Returns:
        The number input widget's return value (int or float)

    Raises:
        UrlParamError: If URL value is invalid, out of bounds, or of wrong type
        ValueError: If min/max values are invalid
    """
    # Get number input parameters
    min_value = bound_args.arguments.get("min_value", None)
    max_value = bound_args.arguments.get("max_value", None)
    value = bound_args.arguments.get("value", _DEFAULT_VALUE)

    # Determine input type (defaults to float)
    input_type: Type[Union[int, float]] = float

    # Check if we can determine type from existing values
    option_types = set()
    if min_value is not None:
        option_types.add(type(min_value))
    if max_value is not None:
        option_types.add(type(max_value))
    if value not in (None, "min"):
        option_types.add(type(value))

    # If we have consistent types, use that type
    if len(option_types) == 1:
        input_type = option_types.pop()
        if input_type not in (int, float):
            raise UrlParamError(
                f"Unsupported number_input type for parameter '{url_key}': {input_type}. Expected int or float."
            )

    # Determine default value if not provided in URL
    if not url_value:
        # Calculate default value based on Streamlit's behavior
        if value == "min":
            if min_value is not None:
                default_value = min_value
            else:
                default_value = 0 if input_type == int else 0.0
        else:
            default_value = (
                value if value is not None else (0 if input_type == int else 0.0)
            )

        init_url_value(url_key, compressor(to_url_value(default_value)))
        return base_widget(**bound_args.arguments)

    url_value = decompressor(url_value)

    validate_single_url_value(url_key, url_value, _HANDLER_NAME)

    try:
        # Parse value based on determined type
        parsed_value = input_type(float(url_value[0]))

        # Validate against min/max constraints
        if min_value is not None and parsed_value < min_value:
            raise UrlParamError(
                f"Value {parsed_value} for {_HANDLER_NAME} parameter '{url_key}' "
                f"is less than min allowed value {min_value}."
            )
        if max_value is not None and parsed_value > max_value:
            raise UrlParamError(
                f"Value {parsed_value} for {_HANDLER_NAME} parameter '{url_key}' "
                f"is greater than max allowed value {max_value}."
            )

        bound_args.arguments["value"] = parsed_value

    except ValueError as err:
        raise UrlParamError(
            f"Invalid value for {_HANDLER_NAME} parameter '{url_key}': {url_value[0]}. "
            f"Expected {input_type.__name__} value. Error: {str(err)}"
        ) from err

    return base_widget(**bound_args.arguments)
