from typing import List, Optional
import inspect
import streamlit as st

from ..utils import init_url_value, validate_single_url_value
from ..exceptions import UrlParamError

def handle_text_input(url_key: str, url_value: Optional[str], bound_args: inspect.BoundArguments):
    """
    Handle text input widget URL state.

    Args:
        url_key: URL parameter key
        url_value: URL parameter value(s)
        bound_args: Bound arguments for the text input widget
    """

    if not url_value:
        value = bound_args.arguments.get("value", "")
        init_url_value(url_key, value)
        return st.text_input(**bound_args.arguments)

    validate_single_url_value(url_key, url_value, 'text_input')
    value = url_value[0]
    max_chars = bound_args.arguments.get('max_chars')
    
    if max_chars is not None and len(value) > max_chars:
        raise UrlParamError(
            f"Invalid value for text_input parameter '{url_key}': "
            f"length ({len(value)}) exceeds maximum allowed characters ({max_chars})."
        )

    bound_args.arguments['value'] = value
    return st.text_input(**bound_args.arguments)