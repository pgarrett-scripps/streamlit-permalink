"""
Streamlit widgets that are aware of URL parameters.
"""

__version__ = "1.0.1"

from typing import Any

# Import all streamlit_permalink modules
from .widgets import *
from .utils import _EMPTY, _NONE


def __getattr__(name: str) -> Any:
    try:
        return getattr(st, name)
    except AttributeError as err:
        raise AttributeError(
            str(err).replace("streamlit", "streamlit_permalink")
        ) from err
