from streamlit.testing.v1 import AppTest
from packaging.version import parse as V
import streamlit as st
import pytest
from .utils import get_query_params, set_query_params


def create_checkbox_app():
    import streamlit as st
    import streamlit_permalink as stp

    stp.checkbox("Test Checkbox", url_key="check")

class TestCheckbox:
    def setup_method(self):
        self.at = AppTest.from_function(create_checkbox_app)

    def test_checkbox_default_state(self):
        """Test checkbox with no URL parameters"""
        self.at.run()

        assert not self.at.exception
        
        # Verify checkbox exists and is unchecked by default
        assert len(self.at.checkbox) == 1
        assert self.at.checkbox[0].value is False
        # Verify URL parameters are empty
        assert not get_query_params(self.at)

    def test_checkbox_url_param_true(self):
        """Test checkbox with URL parameter set to True"""
        # Set initial URL parameter
        set_query_params(self.at, {"check": "True"})
        self.at.run()
        
        # Verify checkbox reflects URL state
        assert self.at.checkbox[0].value is True

    def test_checkbox_url_param_false(self):
        """Test checkbox with URL parameter set to False"""
        set_query_params(self.at, {"check": "False"})
        self.at.run()
        
        assert self.at.checkbox[0].value is False

    def test_checkbox_interaction_updates_url(self):
        """Test that checking/unchecking updates URL parameters"""
        self.at.run()
        
        # Initially unchecked and no URL params
        assert self.at.checkbox[0].value is False
        assert not get_query_params(self.at)
        
        # Check the checkbox
        self.at.checkbox[0].check().run()
        
        # Verify URL parameter was updated
        assert get_query_params(self.at)["check"] == ["True"]
        assert self.at.checkbox[0].value is True
        
        # Uncheck the checkbox
        self.at.checkbox[0].uncheck().run()
        
        # Verify URL parameter was updated
        assert get_query_params(self.at)["check"] == ["False"]
        assert self.at.checkbox[0].value is False

def create_form_checkbox_app():
    import streamlit as st
    import streamlit_permalink as stp

    form = stp.form("test_form")
    with form:
        checkbox = form.checkbox("Form Checkbox", url_key="form_check")
        submitted = form.form_submit_button("Submit")

class TestFormCheckbox:
    def setup_method(self):
        self.at = AppTest.from_function(create_form_checkbox_app)

    def test_form_checkbox_default_state(self):
        """Test form checkbox with no URL parameters"""
        self.at.run()

        assert not self.at.exception
        
        # Verify checkbox exists and is unchecked by default
        assert len(self.at.checkbox) == 1
        assert self.at.checkbox[0].value is False
        # Verify URL parameters are empty
        assert not get_query_params(self.at)

    def test_form_checkbox_url_param_true(self):
        """Test form checkbox with URL parameter set to True"""
        set_query_params(self.at, {"form_check": "True"})
        self.at.run()
        
        assert self.at.checkbox[0].value is True

    def test_form_checkbox_url_param_false(self):
        """Test form checkbox with URL parameter set to False"""
        set_query_params(self.at, {"form_check": "False"})
        self.at.run()
        
        assert self.at.checkbox[0].value is False

    def test_form_checkbox_interaction_updates_url(self):
        """Test that checking/unchecking updates URL parameters after form submission"""
        self.at.run()
        
        # Initially unchecked and no URL params
        assert self.at.checkbox[0].value is False
        assert not get_query_params(self.at)
        
        # Check the checkbox
        self.at.checkbox[0].check()
        # Submit the form
        self.at.button[0].click().run()
        
        # Verify URL parameter was updated after form submission
        assert get_query_params(self.at)["form_check"] == ["True"]
        assert self.at.checkbox[0].value is True
        
        # Uncheck the checkbox
        self.at.checkbox[0].uncheck()
        # Submit the form
        self.at.button[0].click().run()
        
        # Verify URL parameter was updated after form submission
        assert get_query_params(self.at)["form_check"] == ["False"]
        assert self.at.checkbox[0].value is False

    def test_form_checkbox_no_url_update_without_submit(self):
        """Test that URL parameters don't update until form is submitted"""
        self.at.run()
        
        # Initially unchecked and no URL params
        assert self.at.checkbox[0].value is False
        assert not get_query_params(self.at)
        
        # Check the checkbox without submitting
        self.at.checkbox[0].check().run()
        
        # Verify URL parameters haven't changed
        assert not get_query_params(self.at)
        
        # Now submit the form
        self.at.button[0].click().run()
        
        # Verify URL parameters updated after submission
        assert get_query_params(self.at)["form_check"] == ["True"]


