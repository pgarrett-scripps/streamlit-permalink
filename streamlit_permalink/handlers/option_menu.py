from typing import List, Optional
import inspect
import streamlit as st

from ..utils import init_url_value, validate_single_url_value # TODO
from ..exceptions import UrlParamError

def handle_option_menu(url_key: str, url_value: Optional[List[str]], bound_args: inspect.BoundArguments):
    """
    Handle option menu widget URL state.

    Args:
        url_key: URL parameter key
        url_value: URL parameter value(s)
        bound_args: Bound arguments for the option menu widget
    """
    if not url_value:
        # TODO: handle default_index
        return st.option_menu(**bound_args.arguments)

    validate_single_url_value(url_key, url_value, 'option_menu')
    
    value = url_value[0]
    options = list(map(str, bound_args.arguments.get('options', [])))
    
    try:
        bound_args.arguments['default_index'] = options.index(value)
    except ValueError:
        raise UrlParamError(f"Invalid value for option_menu parameter '{url_key}': {value}. Expected one of {options}.")

    return st.option_menu(**bound_args.arguments)