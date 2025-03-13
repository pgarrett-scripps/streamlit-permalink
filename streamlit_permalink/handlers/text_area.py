from typing import List, Optional
import inspect
import streamlit as st

from ..utils import init_url_value, validate_single_url_value
from ..exceptions import UrlParamError


def handle_text_area(url_key: str, url_value: Optional[List[str]], bound_args: inspect.BoundArguments):
    """
    Handle text area widget URL state.

    Args:
        url_key: URL parameter key
        url_value: URL parameter value(s)
        bound_args: Bound arguments for the text area widget
    """
    if not url_value:
        value = bound_args.arguments.get('value', "")
        init_url_value(url_key, value)
        return st.text_area(**bound_args.arguments)

    validate_single_url_value(url_key, url_value, 'text_area')
    value = url_value[0]
    max_chars = bound_args.arguments.get('max_chars')
    
    if max_chars is not None and len(value) > max_chars:
        raise UrlParamError(
            f"Invalid value for text_area parameter '{url_key}': "
            f"length ({len(value)}) exceeds maximum allowed characters ({max_chars})."
        )

    bound_args.arguments['value'] = value
    return st.text_area(**bound_args.arguments)