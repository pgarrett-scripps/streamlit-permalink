from streamlit.testing.v1 import AppTest
from packaging.version import parse as V
import streamlit as st
import pytest
from .utils import get_query_params, set_query_params

def create_color_picker_app():
    import streamlit as st
    import streamlit_permalink as stp

    # Basic color picker with default value
    stp.color_picker("Basic Color", value="#000000", url_key="color")
    
    # Color picker with custom default
    stp.color_picker("Custom Color", value="#FF5733", url_key="custom_color")

def create_form_color_picker_app():
    import streamlit as st
    import streamlit_permalink as stp

    form = stp.form("test_form")
    with form:
        basic_color = form.color_picker("Form Color", 
                                      value="#000000",
                                      url_key="form_color")
        custom_color = form.color_picker("Form Custom Color",
                                       value="#FF5733",
                                       url_key="form_custom_color")
        submitted = form.form_submit_button("Submit")

class TestColorPicker:
    def setup_method(self):
        self.at = AppTest.from_function(create_color_picker_app)

    def test_color_picker_default_state(self):
        """Test color pickers with no URL parameters"""
        self.at.run()

        assert not self.at.exception
        
        # Verify color pickers exist with correct default values
        assert len(self.at.color_picker) == 2
        assert self.at.color_picker[0].value == "#000000"  # Basic color
        assert self.at.color_picker[1].value == "#FF5733"  # Custom color
        # Verify URL parameters are empty
        assert not get_query_params(self.at)

    def test_color_picker_url_params(self):
        """Test color pickers with URL parameters set"""
        # Set initial URL parameters
        set_query_params(self.at, {
            "color": "#FF0000",
            "custom_color": "#00FF00"
        })
        self.at.run()
        
        # Verify color pickers reflect URL state
        assert self.at.color_picker[0].value == "#FF0000"
        assert self.at.color_picker[1].value == "#00FF00"

    def test_color_picker_set_value(self):
        """Test setting specific colors using set_value"""
        self.at.run()
        
        # Set new values with set_value (with #)
        self.at.color_picker[0].set_value("#FF0000").run()
        
        # Verify URL parameters were updated
        params = get_query_params(self.at)
        assert params["color"] == ["#FF0000"]
        assert self.at.color_picker[0].value == "#FF0000"

    def test_color_picker_pick(self):
        """Test setting specific colors using pick"""
        self.at.run()
        
        # Set new values with pick (without #)
        self.at.color_picker[0].pick("00FF00").run()
        
        # Verify URL parameters were updated
        params = get_query_params(self.at)
        assert params["color"] == ["#00FF00"]
        assert self.at.color_picker[0].value == "#00FF00"

class TestFormColorPicker:
    def setup_method(self):
        self.at = AppTest.from_function(create_form_color_picker_app)

    def test_form_color_picker_default_state(self):
        """Test form color pickers with no URL parameters"""
        self.at.run()

        assert not self.at.exception
        
        # Verify color pickers exist with default values
        assert len(self.at.color_picker) == 2
        assert self.at.color_picker[0].value == "#000000"
        assert self.at.color_picker[1].value == "#FF5733"
        # Verify URL parameters are empty
        assert not get_query_params(self.at)

    def test_form_color_picker_url_params(self):
        """Test form color pickers with URL parameters set"""
        set_query_params(self.at, {
            "form_color": "#FF0000",
            "form_custom_color": "#00FF00"
        })
        self.at.run()
        
        assert self.at.color_picker[0].value == "#FF0000"
        assert self.at.color_picker[1].value == "#00FF00"

    def test_form_color_picker_interaction_updates_url(self):
        """Test that changing colors updates URL parameters after form submission"""
        self.at.run()
        
        # Change colors
        self.at.color_picker[0].set_value("#FF0000")
        self.at.color_picker[1].set_value("#00FF00")
        # Submit the form
        self.at.button[0].click().run()
        
        # Verify URL parameters were updated after submission
        params = get_query_params(self.at)
        assert params["form_color"] == ["#FF0000"]
        assert params["form_custom_color"] == ["#00FF00"]
        
        # Change colors again
        self.at.color_picker[0].pick("0000FF")
        self.at.color_picker[1].set_value("#FF0000")
        # Submit again
        self.at.button[0].click().run()
        
        # Verify URL parameters were updated
        params = get_query_params(self.at)
        assert params["form_color"] == ["#0000FF"]
        assert params["form_custom_color"] == ["#FF0000"]

    def test_form_color_picker_no_url_update_without_submit(self):
        """Test that URL parameters don't update until form is submitted"""
        self.at.run()
        
        # Change colors without submitting
        self.at.color_picker[0].set_value("#FF0000")
        self.at.color_picker[1].pick("00FF00").run()
        
        # Verify URL parameters haven't changed
        assert not get_query_params(self.at)
        
        # Submit the form
        self.at.button[0].click().run()
        
        # Verify URL parameters updated after submission
        params = get_query_params(self.at)
        assert params["form_color"] == ["#FF0000"]
        assert params["form_custom_color"] == ["#00FF00"]

    def test_form_color_picker_multiple_changes_before_submit(self):
        """Test that only the final colors before submission are saved to URL"""
        self.at.run()
        
        # Make multiple changes to colors
        self.at.color_picker[0].set_value("#FF0000")
        self.at.color_picker[0].pick("00FF00")
        self.at.color_picker[0].set_value("#0000FF")
        self.at.color_picker[1].set_value("#FF0000")
        self.at.color_picker[1].set_value("#00FF00")
        self.at.color_picker[1].pick("0000FF")
        
        # Submit the form
        self.at.button[0].click().run()
        
        # Verify only final colors are in URL
        params = get_query_params(self.at)
        assert params["form_color"] == ["#0000FF"]
        assert params["form_custom_color"] == ["#0000FF"] 