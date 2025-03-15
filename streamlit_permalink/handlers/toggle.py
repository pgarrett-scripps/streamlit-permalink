from typing import Any, Callable, Dict, List, Optional
import inspect
import streamlit as st

from ..utils import init_url_value, to_url_value, validate_bool_url_value, validate_single_url_value

_DEFAULT_VALUE = False
_HANDLER_NAME = 'toggle'

def handle_toggle(url_key: str, url_value: Optional[List[str]], bound_args: inspect.BoundArguments,
                    compressor: Callable, decompressor: Callable, **kwargs) -> bool:
    """
    Handle toggle widget URL state synchronization.
    
    Manages bidirectional sync between toggle widget state and URL parameters,
    handling validation of boolean values and proper state restoration.

    Args:
        url_key: URL parameter key for this toggle
        url_value: Value(s) from URL, or None if not present
        bound_args: Bound arguments for the toggle widget

    Returns:
        bool: The toggle widget's return value (True if toggled on, False otherwise)
    """
    # Handle the default case when no URL value is provided
    if url_value is None:
        default_value = bound_args.arguments.get('value', _DEFAULT_VALUE)
        init_url_value(url_key, compressor(to_url_value(default_value)))
        return st.toggle(**bound_args.arguments)
    
    url_value = decompressor(url_value)

    # Process and validate the URL value
    url_value_str = validate_single_url_value(url_key, url_value, _HANDLER_NAME)
    url_value_bool = validate_bool_url_value(url_key, url_value_str, _HANDLER_NAME)

    # Update the bound arguments with the validated value
    bound_args.arguments['value'] = url_value_bool
    return st.toggle(**bound_args.arguments)