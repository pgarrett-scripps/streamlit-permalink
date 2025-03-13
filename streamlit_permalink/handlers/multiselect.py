from typing import List, Optional
import inspect
import streamlit as st

from ..utils import _validate_multi_default, _validate_multi_options, _validate_multi_url_values, init_url_value

_HANDLER_NAME = 'multiselect'

def handle_multiselect(url_key: str, url_value: Optional[List[str]], bound_args: inspect.BoundArguments):
    """
    Handle multiselect widget URL state.

    Args:
        url_key: URL parameter key
        url_value: URL parameter value(s)
        bound_args: Bound arguments for the multiselect widget
        
    Returns:
        Streamlit multiselect widget
        
    Raises:
        ValueError: If options are invalid
        UrlParamError: If URL values are invalid
    """
    # Get and validate options
    options = bound_args.arguments.get('options')
    str_options: List[str] = _validate_multi_options(options, _HANDLER_NAME)
    
    # Get and validate default values
    default = bound_args.arguments.get('default')
    str_default: List[str] = _validate_multi_default(default, options, _HANDLER_NAME)    
    
    # If no URL value is provided, initialize with default value
    if url_value is None:
        init_url_value(url_key, default)
        return st.multiselect(**bound_args.arguments)
    
    # Validate URL values against options
    url_values: List[str] = _validate_multi_url_values(url_key, url_value, str_options, _HANDLER_NAME)

    # Convert string values back to original option values
    # Create mapping once instead of in each iteration
    options_map = {str(v): v for v in options}
    actual_url_values = [options_map[v] for v in url_values]
    
    # Update bound arguments with validated values
    bound_args.arguments['default'] = actual_url_values
    return st.multiselect(**bound_args.arguments)
