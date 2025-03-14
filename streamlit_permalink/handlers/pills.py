from typing import Any, List, Optional, Union
import inspect
import streamlit as st

from ..utils import _validate_selection_mode, init_url_value, _validate_multi_options, _validate_multi_default, _validate_multi_url_values

_HANDLER_NAME = 'pills'
_DEFAULT_DEFAULT = None
_DEFAULT_SELECTION_MODE = 'single'

def handle_pills(url_key: str, url_value: Optional[List[str]], bound_args: inspect.BoundArguments) -> Union[List, Any, None]:
    """
    Handle pills widget URL state synchronization.
    
    Manages bidirectional sync between pills widget state and URL parameters,
    supporting both single and multi-selection modes. Handles validation of options
    and conversion between string representations and actual option values.

    Args:
        url_key: URL parameter key for this pills widget
        url_value: Value(s) from URL, or None if not present
        bound_args: Bound arguments for the pills widget
        
    Returns:
        The pills widget's return value (selected option or list of options)
        
    Raises:
        ValueError: If options or selection_mode are invalid
        UrlParamError: If URL values are invalid
    """
    options = bound_args.arguments.get('options')
    str_options: List[str] = _validate_multi_options(options, _HANDLER_NAME)
    
    # Get and validate default values
    default = bound_args.arguments.get('default', _DEFAULT_DEFAULT)
    str_default: List[str] = _validate_multi_default(default, options, _HANDLER_NAME)    

    # Get selection mode (default is 'single')
    selection_mode = _validate_selection_mode(bound_args.arguments.get('selection_mode', _DEFAULT_SELECTION_MODE))
    if selection_mode == 'single' and len(str_default) > 1:
        raise ValueError(f"Invalid default for single-selection {_HANDLER_NAME}: {default}. Expected a single value.")

    # If no URL value is provided, initialize with default value
    if url_value is None:
        init_url_value(url_key, default)
        return st.pills(**bound_args.arguments)
    
    # Validate URL values against options
    url_values: List[str] = _validate_multi_url_values(url_key, url_value, str_options, _HANDLER_NAME)

    # Ensure that the URL value is a single value if selection_mode is 'single'
    if selection_mode == 'single' and len(url_values) > 1:
        raise ValueError(f"Invalid URL value for single-selection {_HANDLER_NAME}: {url_values}. Expected a single value.")
    
    # Convert string values back to original option values
    options_map = {str(v): v for v in options}
    actual_url_values = [options_map[v] for v in url_values]
    
    # Update bound arguments with validated values
    bound_args.arguments['default'] = actual_url_values
    return st.pills(**bound_args.arguments)