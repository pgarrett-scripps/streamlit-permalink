from typing import Any, Callable, Dict, List, Optional, Union
import inspect
import streamlit as st

from ..utils import _validate_multi_default, _validate_multi_options, _validate_multi_url_values, _validate_selection_mode, init_url_value, to_url_value

_HANDLER_NAME = 'segmented_control'

def handle_segmented_control(base_widget, url_key: str, url_value: Optional[List[str]], bound_args: inspect.BoundArguments,
                    compressor: Callable, decompressor: Callable, **kwargs) -> Union[List[Any], Any, None]:
    """
    Handle segmented control widget URL state synchronization.
    
    Manages bidirectional sync between segmented control widget state and URL parameters,
    supporting both single and multi-selection modes. Handles validation of options
    and conversion between string representations and actual option values.
    
    Args:
        url_key: URL parameter key for this segmented control
        url_value: Value(s) from URL, or None if not present
        bound_args: Bound arguments for the segmented control widget
        
    Returns:
        The segmented control widget's return value (selected option or list of options)
        
    Raises:
        ValueError: If options or selection_mode are invalid
        UrlParamError: If URL values are invalid
    """
    # Get and validate options
    options = bound_args.arguments.get('options')
    str_options: List[str] = _validate_multi_options(options, _HANDLER_NAME)
    
    # Get and validate default values
    default = bound_args.arguments.get('default')
    str_default: List[str] = _validate_multi_default(default, options, _HANDLER_NAME)    

    # Get selection mode (default is 'single')
    selection_mode = _validate_selection_mode(bound_args.arguments.get('selection_mode', 'single'))
    if selection_mode == 'single' and len(str_default) > 1:
        raise ValueError(f"Invalid default for single-selection {_HANDLER_NAME}: {default}. Expected a single value.")

    # If no URL value is provided, initialize with default value
    if url_value is None:
        init_url_value(url_key, compressor(to_url_value(default)))
        return base_widget(**bound_args.arguments)
    
    url_value = decompressor(url_value)
    
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
    return base_widget(**bound_args.arguments)
