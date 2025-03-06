from streamlit.testing.v1 import AppTest
from packaging.version import parse as V
import streamlit as st
import pytest
from .utils import get_query_params, set_query_params

def create_segmented_control_app():
    # TODO: Implement when st.segmented_control is released
    pass

def create_form_segmented_control_app():
    # TODO: Implement when st.segmented_control is released
    pass

class TestSegmentedControl:
    def setup_method(self):
        # TODO: Implement when st.segmented_control is released
        self.at = AppTest.from_function(create_segmented_control_app)

    def test_segmented_control_default_state(self):
        """Test segmented control with no URL parameters"""
        # TODO: Implement when st.segmented_control is released
        pass

    def test_segmented_control_url_params(self):
        """Test segmented control with URL parameters set"""
        # TODO: Implement when st.segmented_control is released
        pass

    def test_segmented_control_set_value(self):
        """Test setting specific values"""
        # TODO: Implement when st.segmented_control is released
        pass

class TestFormSegmentedControl:
    def setup_method(self):
        # TODO: Implement when st.segmented_control is released
        self.at = AppTest.from_function(create_form_segmented_control_app)

    def test_form_segmented_control_default_state(self):
        """Test form segmented control with no URL parameters"""
        # TODO: Implement when st.segmented_control is released
        pass

    def test_form_segmented_control_url_params(self):
        """Test form segmented control with URL parameters set"""
        # TODO: Implement when st.segmented_control is released
        pass

    def test_form_segmented_control_interaction_updates_url(self):
        """Test that changing values updates URL parameters after form submission"""
        # TODO: Implement when st.segmented_control is released
        pass

    def test_form_segmented_control_no_url_update_without_submit(self):
        """Test that URL parameters don't update until form is submitted"""
        # TODO: Implement when st.segmented_control is released
        pass

    def test_form_segmented_control_multiple_changes_before_submit(self):
        """Test that only the final values before submission are saved to URL"""
        # TODO: Implement when st.segmented_control is released
        pass 