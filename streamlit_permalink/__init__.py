__version__ = "1.0.0" 

# Import all streamlit_permalink modules
#from .core import *
from .widgets import *
from .utils import _EMPTY, _NONE

def __getattr__(name: str) -> Any:
    try:
        return getattr(st, name)
    except AttributeError as e:
        raise AttributeError(str(e).replace('streamlit', 'streamlit_permalink')) 