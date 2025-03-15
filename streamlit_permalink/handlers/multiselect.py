from typing import Any, Callable, Dict, List, Optional
import inspect
import streamlit as st

from ..utils import _validate_multi_default, _validate_multi_options, _validate_multi_url_values, init_url_value, to_url_value

_HANDLER_NAME = 'multiselect'
_DEFAULT_VALUE = None

def handle_multiselect(base_widget, url_key: str, url_value: Optional[List[str]], bound_args: inspect.BoundArguments,
                    compressor: Callable, decompressor: Callable, **kwargs) -> Any:
    """
    Handle multiselect widget URL state synchronization.
    
    Manages bidirectional sync between multiselect widget state and URL parameters,
    handling validation of options and conversion between string representations and
    actual option values.

    Args:
        url_key: URL parameter key for this multiselect
        url_value: Value(s) from URL, or None if not present
        bound_args: Bound arguments for the multiselect widget
        
    Returns:
        The multiselect widget's return value (list of selected options)
        
    Raises:
        ValueError: If options are invalid
        UrlParamError: If URL values are invalid
    """
    # Get and validate options
    options = bound_args.arguments.get('options')
    str_options: List[str] = _validate_multi_options(options, _HANDLER_NAME)
    
    # Get and validate default values
    default = bound_args.arguments.get('default', _DEFAULT_VALUE)
    str_default: List[str] = _validate_multi_default(default, options, _HANDLER_NAME)    
    
    # If no URL value is provided, initialize with default value
    if url_value is None:
        init_url_value(url_key, compressor(to_url_value(default)))
        return base_widget(**bound_args.arguments)
    
    url_value = decompressor(url_value)
    
    # Validate URL values against options
    url_values: List[str] = _validate_multi_url_values(url_key, url_value, str_options, _HANDLER_NAME)

    # Convert string values back to original option values
    options_map = {str(v): v for v in options}
    actual_url_values = [options_map[v] for v in url_values]
    
    # Update bound arguments with validated values
    bound_args.arguments['default'] = actual_url_values
    return base_widget(**bound_args.arguments)
