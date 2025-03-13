import streamlit as st
from typing import Any
# Instance of UrlAwareForm or None
# used for widgets to know whether they
# are inside a form or not
global _active_form
_active_form = None

def __getattr__(name: str) -> Any:
    try:
        return getattr(st, name)
    except AttributeError as e:
        raise AttributeError(str(e).replace('streamlit', 'streamlit_permalink')) 