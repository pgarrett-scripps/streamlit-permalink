from typing import List, Optional, Any
import inspect
import streamlit as st

from ..utils import init_url_value, validate_single_url_value
from ..exceptions import UrlParamError

_HANDLER_NAME = 'text_area'

def handle_text_area(url_key: str, url_value: Optional[List[str]], bound_args: inspect.BoundArguments) -> str:
    """
    Handle text area widget URL state synchronization.
    
    Manages bidirectional sync between text area widget state and URL parameters,
    handling validation of text length against max_chars constraint if specified.
    
    Args:
        url_key: URL parameter key for this text area
        url_value: Value(s) from URL, or None if not present
        bound_args: Bound arguments for the text area widget
        
    Returns:
        The text area widget's return value (string content)
        
    Raises:
        UrlParamError: If URL value exceeds maximum allowed characters
    """
    if not url_value:
        value = bound_args.arguments.get('value', "")
        init_url_value(url_key, value)
        return st.text_area(**bound_args.arguments)

    validate_single_url_value(url_key, url_value, _HANDLER_NAME)
    value = url_value[0]
    max_chars = bound_args.arguments.get('max_chars')
    
    if max_chars is not None and len(value) > max_chars:
        raise UrlParamError(
            f"Invalid value for {_HANDLER_NAME} parameter '{url_key}': "
            f"length ({len(value)}) exceeds maximum allowed characters ({max_chars})."
        )

    bound_args.arguments['value'] = value
    return st.text_area(**bound_args.arguments)