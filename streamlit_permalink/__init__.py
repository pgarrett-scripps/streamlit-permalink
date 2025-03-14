__version__ = "1.0.0" 

# Import all streamlit_permalink modules
from .core import *
from .widgets import *
from .utils import _EMPTY, _NONE

# Import all streamlit functions and re-export them
import streamlit as _st
import inspect as _inspect
import sys as _sys

# Get all streamlit_permalink attributes
_stp_attributes = set(dir())

# Get all streamlit attributes
_st_attributes = set(dir(_st))

# Find streamlit attributes not in streamlit_permalink
_missing_attributes = _st_attributes - _stp_attributes

# Import missing attributes from streamlit
for _attr in _missing_attributes:
    # Skip private attributes
    if not _attr.startswith('_'):
        # Get the attribute from streamlit
        _st_attr = getattr(_st, _attr)
        
        # Add it to the current module
        setattr(_sys.modules[__name__], _attr, _st_attr)

# Clean up temporary variables
del _st, _inspect, _sys, _stp_attributes, _st_attributes, _missing_attributes, _attr