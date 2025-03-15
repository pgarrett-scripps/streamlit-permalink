from typing import Any, Callable, Dict, List, Optional
import inspect
from streamlit_option_menu import option_menu

from ..utils import _validate_multi_options, init_url_value, to_url_value, validate_single_url_value
from ..exceptions import UrlParamError

"""

def option_menu(menu_title, options, default_index=0, menu_icon=None, icons=None, orientation="vertical",
                styles=None, manual_select=None, key=None, on_change=None):
"""
_HANDLER_NAME = 'option_menu'
_DEFAULT_VALUE = 0

def handle_option_menu(base_widget, url_key: str, url_value: Optional[List[str]], bound_args: inspect.BoundArguments,
                    compressor: Callable, decompressor: Callable, **kwargs) -> Any:
    """
    Handle option menu widget URL state synchronization.
    
    Manages bidirectional sync between option menu widget state and URL parameters,
    handling validation of options and proper indexing of selected values.
    
    Args:
        url_key: URL parameter key for this option menu
        url_value: Value(s) from URL, or None if not present
        bound_args: Bound arguments for the option menu widget
        
    Returns:
        The option menu widget's return value (selected option)
        
    Raises:
        UrlParamError: If URL value is invalid or not in the options list
        ValueError: If options are invalid
    """
    options = bound_args.arguments.get('options')
    str_options: List[str] = _validate_multi_options(options, _HANDLER_NAME)

    index = bound_args.arguments.get('default_index', _DEFAULT_VALUE)
    bound_args.arguments['default_index'] = index

    value = options[index]

    if not url_value:
        init_url_value(url_key, compressor(to_url_value(value)))
        return base_widget(**bound_args.arguments)
    
    url_value = decompressor(url_value)

    url_value_str: Optional[str] = validate_single_url_value(url_key, url_value, _HANDLER_NAME)

    if url_value_str is None:
        raise UrlParamError(f"Invalid value for {_HANDLER_NAME} parameter '{url_key}': {url_value}. Expected a single value.")

    try:
        options_map = {str(v): v for v in options}
        actual_url_value = options_map[url_value_str]
        bound_args.arguments['default_index'] = options.index(actual_url_value)
    except KeyError:
        raise UrlParamError(f"Invalid value for {_HANDLER_NAME} parameter '{url_key}': {url_value_str}. Expected one of {options}.")
    
    return base_widget(**bound_args.arguments)