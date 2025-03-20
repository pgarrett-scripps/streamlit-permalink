"""
Handle time input widget URL state synchronization.
"""

from typing import Any, Callable, List, Optional
import inspect
from datetime import datetime, time

import streamlit as st

from ..constants import _EMPTY, _NONE
from ..utils import init_url_value, to_url_value
from ..exceptions import UrlParamError

_HANDLER_NAME = "time_input"


def _parse_time_from_string(value: str) -> time:
    """Convert string time to time object with only hours and minutes."""
    try:
        # Only accept HH:MM format from URL parameters
        return datetime.strptime(value, "%H:%M").time()
    except ValueError as err:
        raise ValueError(f"Time must be in HH:MM format: {value}") from err


def _parse_time_input_value(value: Any) -> time:
    """Parse input value into a time object, ignoring seconds and microseconds."""
    if value == "now":
        now = datetime.now().time()
        # Ignore seconds and microseconds
        return time(hour=now.hour, minute=now.minute)
    if isinstance(value, str):
        try:
            parsed_time = _parse_time_from_string(value)
            return time(hour=parsed_time.hour, minute=parsed_time.minute)
        except ValueError as err:
            raise ValueError(f"Invalid time format: {str(err)}") from err
    if isinstance(value, datetime):
        # Extract only hours and minutes
        return time(hour=value.hour, minute=value.minute)
    if isinstance(value, time):
        # Extract only hours and minutes
        return time(hour=value.hour, minute=value.minute)

    raise ValueError(
        f"Invalid time value: {value}. Expected a time object, 'now', or a string in HH:MM format."
    )


def handle_time_input(
    base_widget: st.delta_generator.DeltaGenerator,
    url_key: str,
    url_value: Optional[List[str]],
    bound_args: inspect.BoundArguments,
    compressor: Callable,
    decompressor: Callable,
) -> time:
    """
    Handle time input widget URL state synchronization.

    Args:
        base_widget: The base widget to handle
        url_key: Parameter key in URL
        url_value: Value(s) from URL parameter, None if not present
        bound_args: Bound arguments for the base_widget call
        compressor: Compressor function for url_value
        decompressor: Decompressor function for url_value

    Returns:
        The time input widget's return value (time object)

    Raises:
        UrlParamError: If URL value is invalid or not in HH:MM format
    """
    # Extract value from bound arguments (default to "now" if not specified)
    value = bound_args.arguments.get("value", "now")

    # Handle default case when no URL value is provided
    if url_value is None:
        # Parse the original input value, truncating seconds and microseconds
        parsed_value = _parse_time_input_value(value)
        init_url_value(url_key, compressor(to_url_value(parsed_value)))
        return base_widget(**bound_args.arguments)

    url_value = decompressor(url_value)

    # Validate URL value
    if len(url_value) != 1:
        raise UrlParamError(
            f"URL parameter '{url_key}' has {len(url_value)} values, but {_HANDLER_NAME} expects exactly 1 value."
        )

    if url_value[0] == _EMPTY or url_value[0] == _NONE:
        url_value = [None]

    try:
        # Parse time value from URL in HH:MM format only
        parsed_value = _parse_time_from_string(url_value[0])
        bound_args.arguments["value"] = parsed_value
    except ValueError as err:
        raise UrlParamError(
            f"Invalid value for {_HANDLER_NAME} parameter '{url_key}': {url_value[0]}. "
            f"Expected time in format HH:MM."
        ) from err

    return base_widget(**bound_args.arguments)
