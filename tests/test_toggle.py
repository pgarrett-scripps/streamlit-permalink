from streamlit.testing.v1 import AppTest
from packaging.version import parse as V
import streamlit as st
import pytest
from .utils import get_query_params, set_query_params

def create_toggle_app():
    import streamlit as st
    import streamlit_permalink as stp

    stp.toggle("Test Toggle", url_key="toggle")

def create_form_toggle_app():
    import streamlit as st
    import streamlit_permalink as stp

    form = stp.form("test_form")
    with form:
        toggle = form.toggle("Form Toggle", url_key="form_toggle")
        submitted = form.form_submit_button("Submit")

@pytest.mark.skipif(not hasattr(st, 'toggle'), reason="Toggle widget not available in this Streamlit version")
class TestToggle:
    def setup_method(self):
        self.at = AppTest.from_function(create_toggle_app)

    def test_toggle_default_state(self):
        """Test toggle with no URL parameters"""
        self.at.run()

        assert not self.at.exception
        
        # Verify toggle exists and is unchecked by default
        assert len(self.at.toggle) == 1
        assert self.at.toggle[0].value is False
        # Verify URL parameters are empty
        assert not get_query_params(self.at)

    def test_toggle_url_param_true(self):
        """Test toggle with URL parameter set to True"""
        # Set initial URL parameter
        set_query_params(self.at, {"toggle": "True"})
        self.at.run()
        
        # Verify toggle reflects URL state
        assert self.at.toggle[0].value is True

    def test_toggle_url_param_false(self):
        """Test toggle with URL parameter set to False"""
        set_query_params(self.at, {"toggle": "False"})
        self.at.run()
        
        assert self.at.toggle[0].value is False

    def test_toggle_interaction_updates_url(self):
        """Test that toggling on/off updates URL parameters"""
        self.at.run()
        
        # Initially off and no URL params
        assert self.at.toggle[0].value is False
        assert not get_query_params(self.at)
        
        # Turn toggle on
        self.at.toggle[0].set_value(True).run()
        
        # Verify URL parameter was updated
        assert get_query_params(self.at)["toggle"] == ["True"]
        assert self.at.toggle[0].value is True
        
        # Turn toggle off
        self.at.toggle[0].set_value(False).run()
        
        # Verify URL parameter was updated
        assert get_query_params(self.at)["toggle"] == ["False"]
        assert self.at.toggle[0].value is False

@pytest.mark.skipif(not hasattr(st, 'toggle'), reason="Toggle widget not available in this Streamlit version")
class TestFormToggle:
    def setup_method(self):
        self.at = AppTest.from_function(create_form_toggle_app)

    def test_form_toggle_default_state(self):
        """Test form toggle with no URL parameters"""
        self.at.run()

        assert not self.at.exception
        
        # Verify toggle exists and is unchecked by default
        assert len(self.at.toggle) == 1
        assert self.at.toggle[0].value is False
        # Verify URL parameters are empty
        assert not get_query_params(self.at)

    def test_form_toggle_url_param_true(self):
        """Test form toggle with URL parameter set to True"""
        set_query_params(self.at, {"form_toggle": "True"})
        self.at.run()
        
        assert self.at.toggle[0].value is True

    def test_form_toggle_url_param_false(self):
        """Test form toggle with URL parameter set to False"""
        set_query_params(self.at, {"form_toggle": "False"})
        self.at.run()
        
        assert self.at.toggle[0].value is False

    def test_form_toggle_interaction_updates_url(self):
        """Test that toggling updates URL parameters after form submission"""
        self.at.run()
        
        # Initially off and no URL params
        assert self.at.toggle[0].value is False
        assert not get_query_params(self.at)
        
        # Turn toggle on
        self.at.toggle[0].set_value(True)
        # Submit the form
        self.at.button[0].click().run()
        
        # Verify URL parameter was updated after form submission
        assert get_query_params(self.at)["form_toggle"] == ["True"]
        assert self.at.toggle[0].value is True
        
        # Turn toggle off
        self.at.toggle[0].set_value(False)
        # Submit the form
        self.at.button[0].click().run()
        
        # Verify URL parameter was updated after form submission
        assert get_query_params(self.at)["form_toggle"] == ["False"]
        assert self.at.toggle[0].value is False

    def test_form_toggle_no_url_update_without_submit(self):
        """Test that URL parameters don't update until form is submitted"""
        self.at.run()
        
        # Initially off and no URL params
        assert self.at.toggle[0].value is False
        assert not get_query_params(self.at)
        
        # Turn toggle on without submitting
        self.at.toggle[0].set_value(True).run()
        
        # Verify URL parameters haven't changed
        assert not get_query_params(self.at)
        
        # Now submit the form
        self.at.button[0].click().run()
        
        # Verify URL parameters updated after submission
        assert get_query_params(self.at)["form_toggle"] == ["True"] 