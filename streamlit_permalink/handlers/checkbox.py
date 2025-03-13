from typing import List, Optional
import inspect
import streamlit as st

from ..utils import init_url_value, validate_bool_url_value, validate_single_url_value

_HANDLER_NAME = 'checkbox'
_DEFAULT_VALUE = False

def handle_checkbox(url_key: str, url_value: Optional[List[str]], bound_args: inspect.BoundArguments) -> bool:
    """
    Handle checkbox widget URL state.
    
    Synchronizes the checkbox widget state with URL parameters, handling both
    initial rendering and state restoration from URL.

    Args:
        url_key: URL parameter key for this checkbox
        url_value: Value(s) from URL, or None if not present
        bound_args: Bound arguments for the checkbox widget

    Returns:
        A boolean value indicating the state of the checkbox
    """

    # Handle the default case when no URL value is provided
    if url_value is None:
        default_value = bound_args.arguments.get('value', _DEFAULT_VALUE)
        init_url_value(url_key, default_value)
        return st.checkbox(**bound_args.arguments)

    # Process and validate the URL value in a single chain
    url_value: str = validate_single_url_value(url_key, url_value, _HANDLER_NAME)
    url_value: bool = validate_bool_url_value(url_key, url_value, _HANDLER_NAME)

    # Update the bound arguments with the validated value
    bound_args.arguments['value'] = url_value
    return st.checkbox(**bound_args.arguments)