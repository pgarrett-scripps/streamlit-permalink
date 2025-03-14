from typing import Any, List, Optional, Union
import inspect
import streamlit as st

from ..utils import _validate_multi_options, init_url_value, validate_single_url_value
from ..exceptions import UrlParamError

_HANDLER_NAME = 'radio'
_DEFAULT_VALUE = 0

def handle_radio(url_key: str, url_value: Optional[List[str]], bound_args: inspect.BoundArguments) -> Union[Any, None]:
    """
    Handle radio widget URL state synchronization.
    
    Manages bidirectional sync between radio widget state and URL parameters,
    handling validation of options and proper indexing of selected values.
    
    Args:
        url_key: URL parameter key for this radio widget
        url_value: Value(s) from URL, or None if not present
        bound_args: Bound arguments for the radio widget
        
    Returns:
        The radio widget's return value (selected option)
        
    Raises:
        UrlParamError: If URL value is invalid or not in the options list
        ValueError: If options are invalid
    """
    options = bound_args.arguments.get('options')
    str_options: List[str] = _validate_multi_options(options, _HANDLER_NAME)

    index = bound_args.arguments.get('index', _DEFAULT_VALUE)
    bound_args.arguments['index'] = index

    value = options[index]

    if not url_value:
        init_url_value(url_key, value)
        return st.radio(**bound_args.arguments)

    url_value_str: Optional[str] = validate_single_url_value(url_key, url_value, _HANDLER_NAME)

    if url_value_str is not None:
        try:
            # Convert string values back to original option values
            options_map = {str(v): v for v in options}
            actual_url_value = options_map[url_value_str]
            bound_args.arguments['index'] = options.index(actual_url_value)
        except KeyError:
            raise UrlParamError(f"Invalid value for {_HANDLER_NAME} parameter '{url_key}': {url_value_str}. Expected one of {options}.")
    else:
        bound_args.arguments['index'] = None
    
    return st.radio(**bound_args.arguments)