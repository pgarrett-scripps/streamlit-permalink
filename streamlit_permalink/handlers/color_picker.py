from typing import List, Optional
import inspect
import streamlit as st

from ..utils import init_url_value, validate_color_url_value, validate_single_url_value

_DEFAULT_VALUE = '#000000'  # Black (fixed typo)
_HANDLER_NAME = 'color_picker'

def handle_color_picker(url_key: str, url_value: Optional[List[str]], bound_args: inspect.BoundArguments) -> str:
    """
    Handle color picker widget URL state synchronization.
    
    Manages bidirectional sync between color picker widget state and URL parameters,
    initializing URL state on first render and restoring widget state from URL.

    Args:
        url_key: URL parameter key for this color picker
        url_value: Value(s) from URL, or None if not present
        bound_args: Bound arguments for the color picker widget

    Returns:
        str: Selected color in hexadecimal format (e.g. '#000000')

    Raises:
        UrlParamError: If URL value is invalid
    """
    if not url_value:
        default_value = bound_args.arguments.get('value', _DEFAULT_VALUE)
        init_url_value(url_key, default_value)
        return st.color_picker(**bound_args.arguments)

    url_value = validate_single_url_value(url_key, url_value, _HANDLER_NAME)
    url_value = validate_color_url_value(url_key, url_value, _HANDLER_NAME)

    bound_args.arguments['value'] = url_value
    return st.color_picker(**bound_args.arguments)