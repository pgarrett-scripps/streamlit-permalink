"""
Streamlit widgets that are aware of URL parameters.
"""

__version__ = "1.5.0"

from typing import Any

# Import all streamlit_permalink modules
from .widgets import *
from .utils import get_page_url, get_query_params, to_url_value, create_url
from .constants import (
    EMPTY_LIST_URL_VALUE,
    NONE_URL_VALUE,
    EMPTY_STRING_URL_VALUE,
    TRUE_URL_VALUE,
    FALSE_URL_VALUE,
)

def __getattr__(name: str) -> Any:
    try:
        return getattr(st, name)
    except AttributeError as err:
        raise AttributeError(
            str(err).replace("streamlit", "streamlit_permalink")
        ) from err
