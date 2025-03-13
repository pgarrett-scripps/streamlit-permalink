from typing import List, Optional
import inspect
import streamlit as st

from ..utils import init_url_value, validate_single_url_value
from ..exceptions import UrlParamError

def handle_number_input(url_key: str, url_value: Optional[List[str]], bound_args: inspect.BoundArguments):
    """
    Handle number input widget URL state.

    Args:
        url_key: URL parameter key
        url_value: URL parameter value(s)
        bound_args: Bound arguments for the number input widget
    """
    # Get number input parameters
    min_value = bound_args.arguments.get('min_value', None)
    max_value = bound_args.arguments.get('max_value', None)
    value = bound_args.arguments.get('value', "min")
    step = bound_args.arguments.get('step', None)
    
    # Determine input type (defaults to float)
    input_type = float
    
    # Check if we can determine type from existing values
    option_types = set()
    if min_value is not None:
        option_types.add(type(min_value))
    if max_value is not None:
        option_types.add(type(max_value))
    if value not in (None, "min"):
        option_types.add(type(value))
    
    # If we have consistent types, use that type
    if len(option_types) == 1:
        input_type = option_types.pop()
        if input_type not in (int, float):
            raise UrlParamError(f"Unsupported number_input type for parameter '{url_key}': {input_type}. Expected int or float.")
    
    # Determine default value if not provided in URL
    if not url_value:
        # Calculate default value based on Streamlit's behavior
        if value == "min":
            if min_value is not None:
                default_value = min_value
            else:
                default_value = 0 if input_type == int else 0.0
        else:
            default_value = value if value is not None else (0 if input_type == int else 0.0)
        
        init_url_value(url_key, default_value)
        return st.number_input(**bound_args.arguments)
    
    validate_single_url_value(url_key, url_value, 'number_input')

    try:
        # Parse value based on determined type
        parsed_value = input_type(float(url_value[0]))
        
        # Validate against min/max constraints
        if min_value is not None and parsed_value < min_value:
            raise UrlParamError(
                f"Value {parsed_value} for number_input parameter '{url_key}' is less than minimum allowed value {min_value}."
            )
        if max_value is not None and parsed_value > max_value:
            raise UrlParamError(
                f"Value {parsed_value} for number_input parameter '{url_key}' is greater than maximum allowed value {max_value}."
            )
        
        bound_args.arguments['value'] = parsed_value
        
    except ValueError as e:
        raise UrlParamError(
            f"Invalid value for number_input parameter '{url_key}': {url_value[0]}. "
            f"Expected {input_type.__name__} value. Error: {str(e)}"
        )
    
    return st.number_input(**bound_args.arguments)