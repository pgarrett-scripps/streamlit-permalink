from typing import List, Optional
import inspect
import streamlit as st

from ..utils import init_url_value, validate_color_url_value, validate_single_url_value

_DEFAULT_VALUE = '#000000' # Balck
_HANDLER_NAME = 'color_picker'

def handle_color_picker(url_key: str, url_value: Optional[List[str]], bound_args: inspect.BoundArguments) -> str:
    """
    Handle color picker widget URL state.
    
    Synchronizes the color picker widget state with URL parameters, handling both
    initial rendering and state restoration from URL.

    Args:
        url_key: URL parameter key for this color picker
        url_value: Value(s) from URL, or None if not present
        bound_args: Bound arguments for the color picker widget

    Returns:
        str: A color string in hexadecimal format (e.g. '#000000' for black)
    """
    if not url_value:
        default_value = bound_args.arguments.get('value', _DEFAULT_VALUE)
        init_url_value(url_key, default_value)
        return st.color_picker(**bound_args.arguments)

    url_value: str = validate_single_url_value(url_key, url_value, _HANDLER_NAME)
    url_value: str = validate_color_url_value(url_key, url_value, _HANDLER_NAME)

    bound_args.arguments['value'] = url_value
    return st.color_picker(**bound_args.arguments)