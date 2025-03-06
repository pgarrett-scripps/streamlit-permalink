from streamlit.testing.v1 import AppTest
from packaging.version import parse as V
import streamlit as st
import pytest
from .utils import get_query_params, set_query_params

def create_single_slider_app():
    import streamlit as st
    import streamlit_permalink as stp

    stp.slider("Single Value Slider", min_value=0, max_value=100, value=50, url_key="slider")

def create_range_slider_app():
    import streamlit as st
    import streamlit_permalink as stp

    stp.slider("Range Slider", min_value=0, max_value=100, value=(25, 75), url_key="range_slider")

def create_form_slider_app():
    import streamlit as st
    import streamlit_permalink as stp

    form = stp.form("test_form")
    with form:
        single = form.slider("Form Single Slider", min_value=0, max_value=100, value=50, url_key="form_slider")
        range_slider = form.slider("Form Range Slider", min_value=0, max_value=100, value=(25, 75), url_key="form_range")
        submitted = form.form_submit_button("Submit")

class TestSingleSlider:
    def setup_method(self):
        self.at = AppTest.from_function(create_single_slider_app)

    def test_slider_default_state(self):
        """Test single value slider with no URL parameters"""
        self.at.run()

        assert not self.at.exception
        
        # Verify slider exists and has default value
        assert len(self.at.slider) == 1
        assert self.at.slider[0].value == 50
        # Verify URL parameters are empty
        assert not get_query_params(self.at)

    def test_slider_url_param(self):
        """Test slider with URL parameter set"""
        # Set initial URL parameter
        set_query_params(self.at, {"slider": "75"})
        self.at.run()
        
        # Verify slider reflects URL state
        assert self.at.slider[0].value == 75

    def test_slider_interaction_updates_url(self):
        """Test that moving slider updates URL parameters"""
        self.at.run()
        
        # Move slider to new value
        self.at.slider[0].set_value(25).run()
        
        # Verify URL parameter was updated
        assert get_query_params(self.at)["slider"] == ["25"]
        assert self.at.slider[0].value == 25

class TestRangeSlider:
    def setup_method(self):
        self.at = AppTest.from_function(create_range_slider_app)

    def test_range_slider_default_state(self):
        """Test range slider with no URL parameters"""
        self.at.run()

        assert not self.at.exception
        
        # Verify slider exists and has default range
        assert len(self.at.slider) == 1
        assert self.at.slider[0].value == (25, 75)
        # Verify URL parameters are empty
        assert not get_query_params(self.at)

    def test_range_slider_url_param(self):
        """Test range slider with URL parameters set"""
        # Set initial URL parameters
        set_query_params(self.at, {"range_slider": ["30", "80"]})
        self.at.run()
        
        # Verify slider reflects URL state
        assert self.at.slider[0].value == (30, 80)

    def test_range_slider_interaction_updates_url(self):
        """Test that moving range slider updates URL parameters"""
        self.at.run()
        
        # Move range to new values
        self.at.slider[0].set_range(10, 90).run()
        
        # Verify URL parameters were updated
        assert get_query_params(self.at)["range_slider"] == ["10", "90"]
        assert self.at.slider[0].value == (10, 90)

class TestFormSlider:
    def setup_method(self):
        self.at = AppTest.from_function(create_form_slider_app)

    def test_form_sliders_default_state(self):
        """Test form sliders with no URL parameters"""
        self.at.run()

        assert not self.at.exception
        
        # Verify sliders exist with default values
        assert len(self.at.slider) == 2
        assert self.at.slider[0].value == 50  # Single value slider
        assert self.at.slider[1].value == (25, 75)  # Range slider
        # Verify URL parameters are empty
        assert not get_query_params(self.at)

    def test_form_sliders_url_param(self):
        """Test form sliders with URL parameters set"""
        set_query_params(self.at, {
            "form_slider": "60",
            "form_range": ["20", "85"]
        })
        self.at.run()
        
        assert self.at.slider[0].value == 60
        assert self.at.slider[1].value == (20, 85)

    def test_form_slider_interaction_updates_url(self):
        """Test that moving sliders updates URL parameters after form submission"""
        self.at.run()
        
        # Move both sliders
        self.at.slider[0].set_value(75)
        self.at.slider[1].set_range(40, 95)
        # Submit the form
        self.at.button[0].click().run()
        
        # Verify URL parameters were updated after submission
        params = get_query_params(self.at)
        assert params["form_slider"] == ["75"]
        assert params["form_range"] == ["40", "95"]
        
        # Move sliders again
        self.at.slider[0].set_value(30)
        self.at.slider[1].set_range(15, 60)
        # Submit again
        self.at.button[0].click().run()
        
        # Verify URL parameters were updated
        params = get_query_params(self.at)
        assert params["form_slider"] == ["30"]
        assert params["form_range"] == ["15", "60"]

    def test_form_slider_no_url_update_without_submit(self):
        """Test that URL parameters don't update until form is submitted"""
        self.at.run()
        
        # Move sliders without submitting
        self.at.slider[0].set_value(45)
        self.at.slider[1].set_range(35, 65).run()
        
        # Verify URL parameters haven't changed
        assert not get_query_params(self.at)
        
        # Submit the form
        self.at.button[0].click().run()
        
        # Verify URL parameters updated after submission
        params = get_query_params(self.at)
        assert params["form_slider"] == ["45"]
        assert params["form_range"] == ["35", "65"]

    def test_form_slider_multiple_changes_before_submit(self):
        """Test that only the final slider positions before submission are saved to URL"""
        self.at.run()
        
        # Make multiple changes to sliders
        self.at.slider[0].set_value(20)
        self.at.slider[0].set_value(40)
        self.at.slider[0].set_value(30)
        self.at.slider[1].set_range(10, 50)
        self.at.slider[1].set_range(30, 70)
        self.at.slider[1].set_range(20, 60)
        
        # Submit the form
        self.at.button[0].click().run()
        
        # Verify only final positions are in URL
        params = get_query_params(self.at)
        assert params["form_slider"] == ["30"]
        assert params["form_range"] == ["20", "60"] 