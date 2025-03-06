import streamlit as st

# Instance of UrlAwareForm or None
# used for widgets to know whether they
# are inside a form or not
global _active_form
_active_form = None

def __getattr__(name):
    try:
        return getattr(st, name)
    except AttributeError as e:
        raise AttributeError(str(e).replace('streamlit', 'streamlit_permalink')) 