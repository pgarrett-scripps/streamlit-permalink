import streamlit as st
from typing import Any, Optional, ContextManager
from contextlib import contextmanager

# Replace global variable with a class to manage form state
class FormStateManager:
    def __init__(self):
        self.active_form = None
    
    @contextmanager
    def set_active_form(self, form):
        """Context manager to set and clear the active form."""
        previous_form = self.active_form
        self.active_form = form
        try:
            yield
        finally:
            self.active_form = previous_form
    
    def get_active_form(self):
        """Get the currently active form."""
        return self.active_form

# Singleton instance of the form state manager
form_state = FormStateManager()

def __getattr__(name: str) -> Any:
    try:
        return getattr(st, name)
    except AttributeError as e:
        raise AttributeError(str(e).replace('streamlit', 'streamlit_permalink')) 