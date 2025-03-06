from streamlit.testing.v1 import AppTest
from packaging.version import parse as V
import streamlit as st
import pytest
from .utils import get_query_params, set_query_params

def create_pills_app():
    # TODO: Implement when st.pills is released
    pass

def create_form_pills_app():
    # TODO: Implement when st.pills is released
    pass

class TestPills:
    def setup_method(self):
        # TODO: Implement when st.pills is released
        self.at = AppTest.from_function(create_pills_app)

    def test_pills_default_state(self):
        """Test pills with no URL parameters"""
        # TODO: Implement when st.pills is released
        pass

    def test_pills_url_params(self):
        """Test pills with URL parameters set"""
        # TODO: Implement when st.pills is released
        pass

    def test_pills_set_value(self):
        """Test setting specific values"""
        # TODO: Implement when st.pills is released
        pass

class TestFormPills:
    def setup_method(self):
        # TODO: Implement when st.pills is released
        self.at = AppTest.from_function(create_form_pills_app)

    def test_form_pills_default_state(self):
        """Test form pills with no URL parameters"""
        # TODO: Implement when st.pills is released
        pass

    def test_form_pills_url_params(self):
        """Test form pills with URL parameters set"""
        # TODO: Implement when st.pills is released
        pass

    def test_form_pills_interaction_updates_url(self):
        """Test that changing pills updates URL parameters after form submission"""
        # TODO: Implement when st.pills is released
        pass

    def test_form_pills_no_url_update_without_submit(self):
        """Test that URL parameters don't update until form is submitted"""
        # TODO: Implement when st.pills is released
        pass

    def test_form_pills_multiple_changes_before_submit(self):
        """Test that only the final values before submission are saved to URL"""
        # TODO: Implement when st.pills is released
        pass 