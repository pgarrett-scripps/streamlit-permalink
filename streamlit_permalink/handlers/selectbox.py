from typing import Any, Callable, Dict, List, Optional
import inspect
import streamlit as st

from ..utils import _validate_multi_options, init_url_value, to_url_value, validate_single_url_value
from ..exceptions import UrlParamError

_HANDLER_NAME = 'selectbox'

def handle_selectbox(url_key: str, url_value: Optional[List[str]], bound_args: inspect.BoundArguments,
                    compressor: Callable, decompressor: Callable, **kwargs):
    """
    Handle selectbox widget URL state.

    Args:
        url_key: URL parameter key
        url_value: URL parameter value(s)
        bound_args: Bound arguments for the selectbox widget
    """

    options = bound_args.arguments.get('options')
    str_options: List[str] = _validate_multi_options(options, _HANDLER_NAME)

    index = bound_args.arguments.get('index', 0)
    bound_args.arguments['index'] = index

    value = options[index]

    if not url_value:
        init_url_value(url_key, compressor(to_url_value(value)))
        return st.selectbox(**bound_args.arguments)
    
    url_value = decompressor(url_value)

    url_value: Optional[str] = validate_single_url_value(url_key, url_value, _HANDLER_NAME)

    if url_value is not None:
        try:
            options_map = {str(v): v for v in options}
            actual_url_value = options_map[url_value]
            bound_args.arguments['index'] = options.index(actual_url_value)
        except KeyError:
            raise UrlParamError(f"Invalid value for {_HANDLER_NAME} parameter '{url_key}': {url_value}. Expected one of {options}.")
    else:
        bound_args.arguments['index'] = None
    
    return st.selectbox(**bound_args.arguments)
