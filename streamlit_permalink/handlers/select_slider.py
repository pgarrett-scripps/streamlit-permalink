from typing import Any, Callable, Dict, List, Optional, Union, Tuple    
import inspect
import streamlit as st

from ..utils import _validate_multi_default, _validate_multi_options, _validate_multi_url_values, init_url_value, to_url_value
from ..exceptions import UrlParamError

_HANDLER_NAME = 'select_slider'

def handle_select_slider(url_key: str, url_value: Optional[List[str]], bound_args: inspect.BoundArguments,
                    compressor: Callable, decompressor: Callable, **kwargs) -> Any:
    """
    Handle select slider widget URL state synchronization.
    
    Manages bidirectional sync between select slider widget state and URL parameters,
    supporting both single value and range selection modes. Handles validation of options
    and ensures proper ordering of range values.
    
    Args:
        url_key: URL parameter key for this select slider
        url_value: Value(s) from URL, or None if not present
        bound_args: Bound arguments for the select slider widget
        
    Returns:
        The select slider widget's return value (selected option or range)
        
    Raises:
        ValueError: If options or values are invalid
        UrlParamError: If URL values are invalid or out of order
    """
    # Get and validate options
    options = bound_args.arguments.get('options')
    str_options: List[str] = _validate_multi_options(options, _HANDLER_NAME)

    # Get value
    value = bound_args.arguments.get('value')
    
    # Normalize value to a list
    if value is None:
        value = [options[0]]
    elif isinstance(value, (list, tuple)):
        value = list(value)
    else:
        value = [value]

    is_range_slider = len(value) == 2

    # Validate value length
    if is_range_slider and len(value) != 2:
        raise ValueError(f"Invalid value for {_HANDLER_NAME} parameter '{url_key}': {value}. Expected a single value or a tuple of two values.")
    elif not is_range_slider and len(value) != 1:
        raise ValueError(f"Invalid value for {_HANDLER_NAME} parameter '{url_key}': {value}. Expected a single value or a tuple of two values.")
        
    values_str = _validate_multi_default(value, options, _HANDLER_NAME)

    if not url_value:
        init_url_value(url_key, compressor(to_url_value(value)))
        return st.select_slider(**bound_args.arguments)
    
    url_value = decompressor(url_value)

    # Validate URL values against options
    url_values: List[str] = _validate_multi_url_values(url_key, url_value, str_options, _HANDLER_NAME)

    # Validate URL values match expected slider type
    if is_range_slider and len(url_values) != 2:
        raise ValueError(f"Invalid value for {_HANDLER_NAME} parameter '{url_key}': {url_values}. Expected a tuple of two values for range slider.")
    elif not is_range_slider and len(url_values) != 1:
        raise ValueError(f"Invalid value for {_HANDLER_NAME} parameter '{url_key}': {url_values}. Expected a single value for single slider.")

    # Convert string values back to original option values
    options_map = {str(v): v for v in options}
    actual_url_values = [options_map[v] for v in url_values]
    
    # For range sliders, ensure values are in correct order
    if is_range_slider:
        start_idx = options.index(actual_url_values[0])
        end_idx = options.index(actual_url_values[1])
        if start_idx > end_idx:
            raise UrlParamError(
                f"Invalid range for {_HANDLER_NAME} parameter '{url_key}': "
                f"start value '{actual_url_values[0]}' comes after end value '{actual_url_values[1]}' in options."
            )
    
    # Update bound arguments with validated values
    bound_args.arguments['value'] = tuple(actual_url_values) if is_range_slider else actual_url_values[0]
    return st.select_slider(**bound_args.arguments)