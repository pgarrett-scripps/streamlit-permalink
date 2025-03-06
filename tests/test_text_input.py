from streamlit.testing.v1 import AppTest
from packaging.version import parse as V
import streamlit as st
import pytest
from .utils import get_query_params, set_query_params

def create_text_input_app():
    import streamlit as st
    import streamlit_permalink as stp

    stp.text_input("Basic Text Input", value="", url_key="text")
    stp.text_input("Limited Text Input", max_chars=10, url_key="limited_text")
    stp.text_input("Default Value Text", value="default", url_key="default_text")

def create_form_text_input_app():
    import streamlit as st
    import streamlit_permalink as stp

    form = stp.form("test_form")
    with form:
        text = form.text_input("Form Text Input", url_key="form_text")
        limited = form.text_input("Form Limited Text", max_chars=10, url_key="form_limited")
        submitted = form.form_submit_button("Submit")

class TestTextInput:
    def setup_method(self):
        self.at = AppTest.from_function(create_text_input_app)

    def test_text_input_default_state(self):
        """Test text inputs with no URL parameters"""
        self.at.run()

        assert not self.at.exception
        
        # Verify text inputs exist with correct default values
        assert len(self.at.text_input) == 3
        assert self.at.text_input[0].value == ""  # Basic input
        assert self.at.text_input[1].value == ""  # Limited input
        assert self.at.text_input[2].value == "default"  # Default value input
        # Verify URL parameters are empty
        assert not get_query_params(self.at)

    def test_text_input_url_params(self):
        """Test text inputs with URL parameters set"""
        # Set initial URL parameters
        set_query_params(self.at, {
            "text": "hello world",
            "limited_text": "short",
            "default_text": "changed"
        })
        self.at.run()
        
        # Verify text inputs reflect URL state
        assert self.at.text_input[0].value == "hello world"
        assert self.at.text_input[1].value == "short"
        assert self.at.text_input[2].value == "changed"

    def test_text_input_interaction_updates_url(self):
        """Test that typing in text inputs updates URL parameters"""
        self.at.run()
        
        # Type in basic text input
        self.at.text_input[0].set_value("new text").run()
        
        # Verify URL parameter was updated
        assert get_query_params(self.at)["text"] == ["new text"]
        assert self.at.text_input[0].value == "new text"

    def test_text_input_character_limit(self):
        """Test that character limits are enforced"""
        # TODO: Implement this, seems buggy
        pass

    def test_text_input_set_value_bypasses_limit(self):
        """Test that set_value can bypass character limit"""
        # TODO: Implement this, seems buggy
        pass

class TestFormTextInput:
    def setup_method(self):
        self.at = AppTest.from_function(create_form_text_input_app)

    def test_form_text_input_default_state(self):
        """Test form text inputs with no URL parameters"""
        self.at.run()

        assert not self.at.exception
        
        # Verify text inputs exist with empty default values
        assert len(self.at.text_input) == 2
        assert self.at.text_input[0].value == ""
        assert self.at.text_input[1].value == ""
        # Verify URL parameters are empty
        assert not get_query_params(self.at)

    def test_form_text_input_url_params(self):
        """Test form text inputs with URL parameters set"""
        set_query_params(self.at, {
            "form_text": "hello form",
            "form_limited": "short"
        })
        self.at.run()
        
        assert self.at.text_input[0].value == "hello form"
        assert self.at.text_input[1].value == "short"

    def test_form_text_input_interaction_updates_url(self):
        """Test that typing updates URL parameters after form submission"""
        self.at.run()
        
        # Type in text inputs
        self.at.text_input[0].set_value("form text")
        self.at.text_input[1].input("limited")
        # Submit the form
        self.at.button[0].click().run()
        
        # Verify URL parameters were updated after submission
        params = get_query_params(self.at)
        assert params["form_text"] == ["form text"]
        assert params["form_limited"] == ["limited"]
        
        # Change text and submit again
        self.at.text_input[0].set_value("new text")
        self.at.text_input[1].input("new")
        self.at.button[0].click().run()
        
        # Verify URL parameters were updated
        params = get_query_params(self.at)
        assert params["form_text"] == ["new text"]
        assert params["form_limited"] == ["new"]

    def test_form_text_input_no_url_update_without_submit(self):
        """Test that URL parameters don't update until form is submitted"""
        self.at.run()
        
        # Type in text inputs without submitting
        self.at.text_input[0].set_value("unsubmitted")
        self.at.text_input[1].input("waiting").run()
        
        # Verify URL parameters haven't changed
        assert not get_query_params(self.at)
        
        # Submit the form
        self.at.button[0].click().run()
        
        # Verify URL parameters updated after submission
        params = get_query_params(self.at)
        assert params["form_text"] == ["unsubmitted"]
        assert params["form_limited"] == ["waiting"]

    def test_form_text_input_multiple_changes_before_submit(self):
        """Test that only the final text before submission is saved to URL"""
        self.at.run()
        
        # Make multiple changes to text inputs
        self.at.text_input[0].set_value("first")
        self.at.text_input[0].set_value("second")
        self.at.text_input[0].set_value("final")
        self.at.text_input[1].input("one")
        self.at.text_input[1].input("two")
        self.at.text_input[1].input("last")
        
        # Submit the form
        self.at.button[0].click().run()
        
        # Verify only final text is in URL
        params = get_query_params(self.at)
        assert params["form_text"] == ["final"]
        assert params["form_limited"] == ["last"]

    def test_form_text_input_character_limit(self):
        """Test that character limits are enforced in forms"""
        # TODO: Implement this, seems buggy
        pass