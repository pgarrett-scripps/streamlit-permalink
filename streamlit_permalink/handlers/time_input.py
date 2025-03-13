from typing import List, Optional, Any
import inspect
import streamlit as st
from datetime import datetime, time

from streamlit_permalink.constants import _EMPTY, _NONE

from ..utils import init_url_value
from ..exceptions import UrlParamError

def _parse_time_from_string(value: str) -> time:
    """Convert string time to time object with only hours and minutes."""
    try:
        # Only accept HH:MM format from URL parameters
        return datetime.strptime(value, "%H:%M").time()
    except ValueError:
        raise ValueError(f"Time must be in HH:MM format: {value}")

def _parse_time_input_value(value: Any) -> time:
    """Parse input value into a time object, ignoring seconds and microseconds."""
    if value == "now":
        now = datetime.now().time()
        # Ignore seconds and microseconds
        return time(hour=now.hour, minute=now.minute)
    elif isinstance(value, str):
        try:
            parsed_time = _parse_time_from_string(value)
            return time(hour=parsed_time.hour, minute=parsed_time.minute)
        except ValueError as e:
            raise ValueError(f"Invalid time format: {str(e)}")
    elif isinstance(value, datetime):
        # Extract only hours and minutes
        return time(hour=value.hour, minute=value.minute)
    elif isinstance(value, time):
        # Extract only hours and minutes
        return time(hour=value.hour, minute=value.minute)
    else:
        raise ValueError(f"Invalid time value: {value}. Expected a time object, 'now', or a string in HH:MM format.")

def handle_time_input(url_key: str, url_value: Optional[List[str]], bound_args: inspect.BoundArguments):
    """
    Handle time input widget URL state.

    Args:
        url_key: URL parameter key
        url_value: URL parameter value(s)
        bound_args: Bound arguments for the time input widget
    """
    # Extract value from bound arguments (default to "now" if not specified)
    value = bound_args.arguments.get('value', "now")
    
    # Handle default case when no URL value is provided
    if url_value is None:
        # Parse the original input value, truncating seconds and microseconds
        parsed_value = _parse_time_input_value(value)
        init_url_value(url_key, parsed_value)
        return st.time_input(**bound_args.arguments)
    
    # Validate URL value
    if len(url_value) != 1:
        raise UrlParamError(f"URL parameter '{url_key}' has {len(url_value)} values, but time_input expects exactly 1 value.")
    
    if url_value[0] == _EMPTY or url_value[0] == _NONE:
        url_value = [None]

    try:
        # Parse time value from URL in HH:MM format only
        parsed_value = _parse_time_from_string(url_value[0])
        bound_args.arguments['value'] = parsed_value
    except ValueError:
        raise UrlParamError(
            f"Invalid value for time_input parameter '{url_key}': {url_value[0]}. "
            f"Expected time in format HH:MM."
        )
    
    return st.time_input(**bound_args.arguments)