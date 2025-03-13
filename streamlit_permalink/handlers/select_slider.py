from typing import List, Optional
import inspect
import streamlit as st

from ..utils import _validate_multi_default, _validate_multi_options, _validate_multi_url_values, init_url_value
from ..exceptions import UrlParamError

_HANDLER_NAME = 'select_slider'

def handle_select_slider(url_key: str, url_value: Optional[List[str]], bound_args: inspect.BoundArguments):
    """
    Handle select slider widget URL state.

    Args:
        url_key: URL parameter key
        url_value: URL parameter value(s)
        bound_args: Bound arguments for the select slider widget
    """

    # Get and validate options
    options = bound_args.arguments.get('options')
    str_options: List[str] = _validate_multi_options(options, _HANDLER_NAME)

    # get value
    value = bound_args.arguments.get('value') # can by any, (list, tuple), None
    
    # value is not none and is a list
    if value is None:
        value = [options[0]]
    elif isinstance(value, (list, tuple)):
        value = list(value)
    else:
        value = [value]

    is_range_slider = len(value) == 2

    if is_range_slider:
        # ensure that value is len 2 or throw Value Error
        if len(value) != 2:
            raise ValueError(f"Invalid value for {_HANDLER_NAME} parameter '{url_key}': {value}. Expected a single value or a tuple of two values.")
    else:
        # ensure that value is len 1 or throw Value Error
        if len(value) != 1:
            raise ValueError(f"Invalid value for {_HANDLER_NAME} parameter '{url_key}': {value}. Expected a single value or a tuple of two values.")
        
    values_str = _validate_multi_default(value, options, _HANDLER_NAME)

    if not url_value:
        init_url_value(url_key, value)
        return st.select_slider(**bound_args.arguments)
    
    # Validate URL values against options
    url_values: List[str] = _validate_multi_url_values(url_key, url_value, str_options, _HANDLER_NAME)

    if is_range_slider and len(url_values) != 2:
        raise ValueError(f"Invalid value for {_HANDLER_NAME} parameter '{url_key}': {url_values}. Expected a single value or a tuple of two values.")
    elif not is_range_slider and len(url_values) != 1:
        raise ValueError(f"Invalid value for {_HANDLER_NAME} parameter '{url_key}': {url_values}. Expected a single value or a tuple of two values.")

    # Convert string values back to original option values
    # Create mapping once instead of in each iteration
    options_map = {str(v): v for v in options}
    actual_url_values = [options_map[v] for v in url_values]
    
    # Update bound arguments with validated values
    bound_args.arguments['value'] = actual_url_values if is_range_slider else actual_url_values[0]
    return st.select_slider(**bound_args.arguments)

    # Convert options to strings for comparison
    options = list(map(str, bound_args.arguments.get('options', [])))
    bound_args.arguments['options'] = options
    
    if not url_value:
        value = bound_args.arguments.get('value')
        if isinstance(value, (list, tuple)):
            init_url_value(url_key, [str(value[0]), str(value[1])])
        else:
            init_url_value(url_key, str(value) if value is not None else str(options[0]))
        return st.select_slider(**bound_args.arguments)

    # Determine if this is a range slider based on the initial value
    value = bound_args.arguments.get('value')
    is_range_slider = isinstance(value, (list, tuple)) if value is not None else False
    expected_values = 2 if is_range_slider else 1

    # Validate number of values matches slider type
    if len(url_value) != expected_values:
        raise UrlParamError(
            f"Invalid number of values for select_slider parameter '{url_key}': got {len(url_value)}, "
            f"expected {expected_values} ({'range' if is_range_slider else 'single'} slider)"
        )

    # Validate values are in options
    invalid_values = [v for v in url_value if v not in options]
    if invalid_values:
        raise UrlParamError(
            f"Invalid value(s) for select_slider parameter '{url_key}': {invalid_values}. "
            f"Expected values from {options}."
        )

    # Set value based on slider type
    if is_range_slider:
        # Ensure range values are in correct order based on options order
        start_idx = options.index(url_value[0])
        end_idx = options.index(url_value[1])
        if start_idx > end_idx:
            raise UrlParamError(
                f"Invalid range for select_slider parameter '{url_key}': "
                f"start value '{url_value[0]}' comes after end value '{url_value[1]}' in options."
            )
        bound_args.arguments['value'] = tuple(url_value)
    else:
        bound_args.arguments['value'] = url_value[0]

    return st.select_slider(**bound_args.arguments)