from streamlit.testing.v1 import AppTest
from packaging.version import parse as V
import streamlit as st
import pytest
from .utils import get_query_params, set_query_params

def create_multiselect_app():
    import streamlit as st
    import streamlit_permalink as stp

    OPTIONS = ["Option A", "Option B", "Option C", "Option D"]
    stp.multiselect("Test Multiselect", options=OPTIONS, url_key="multi")

def create_form_multiselect_app():
    import streamlit as st
    import streamlit_permalink as stp

    form = stp.form("test_form")
    with form:
        OPTIONS = ["Option A", "Option B", "Option C", "Option D"]
        multiselect = form.multiselect("Form Multiselect", options=OPTIONS, url_key="form_multi")
        submitted = form.form_submit_button("Submit")

class TestMultiselect:
    def setup_method(self):
        self.at = AppTest.from_function(create_multiselect_app)
        self.OPTIONS = ["Option A", "Option B", "Option C", "Option D"]

    def test_multiselect_default_state(self):
        """Test multiselect with no URL parameters"""
        self.at.run()

        assert not self.at.exception
        
        # Verify multiselect exists and starts empty
        assert len(self.at.multiselect) == 1
        assert self.at.multiselect[0].value == []
        assert self.at.multiselect[0].indices == []
        # Verify URL parameters are empty
        assert not get_query_params(self.at)

    def test_multiselect_url_param(self):
        """Test multiselect with URL parameters set"""
        # Set initial URL parameters with multiple selections
        set_query_params(self.at, {"multi": ["Option A", "Option C"]})
        self.at.run()
        
        # Verify multiselect reflects URL state
        assert self.at.multiselect[0].value == ["Option A", "Option C"]
        assert self.at.multiselect[0].indices == [0, 2]

    def test_multiselect_select_interaction(self):
        """Test selecting individual options"""
        self.at.run()
        
        # Initially empty
        assert self.at.multiselect[0].value == []
        
        # Select first option
        self.at.multiselect[0].select("Option A").run()
        assert get_query_params(self.at)["multi"] == ["Option A"]
        assert self.at.multiselect[0].value == ["Option A"]
        
        # Select additional option
        self.at.multiselect[0].select("Option C").run()
        assert get_query_params(self.at)["multi"] == ["Option A", "Option C"]
        assert self.at.multiselect[0].value == ["Option A", "Option C"]

    def test_multiselect_unselect_interaction(self):
        """Test unselecting options"""
        self.at.run()
        
        # Start with multiple selections
        self.at.multiselect[0].set_value(["Option A", "Option B", "Option C"]).run()
        assert len(self.at.multiselect[0].value) == 3
        
        # Unselect middle option
        self.at.multiselect[0].unselect("Option B").run()
        assert get_query_params(self.at)["multi"] == ["Option A", "Option C"]
        assert self.at.multiselect[0].value == ["Option A", "Option C"]
        
        # Unselect all remaining options
        self.at.multiselect[0].set_value([]).run()
        # Empty list is represented by _STREAMLIT_PERMALINK_EMPTY in URL
        assert get_query_params(self.at)["multi"] == ["_STREAMLIT_PERMALINK_EMPTY"]
        assert self.at.multiselect[0].value == []

    def test_multiselect_set_value_interaction(self):
        """Test setting multiple values at once"""
        self.at.run()
        
        # Set multiple values
        self.at.multiselect[0].set_value(["Option B", "Option D"]).run()
        assert get_query_params(self.at)["multi"] == ["Option B", "Option D"]
        assert self.at.multiselect[0].value == ["Option B", "Option D"]
        assert self.at.multiselect[0].indices == [1, 3]

class TestFormMultiselect:
    def setup_method(self):
        self.at = AppTest.from_function(create_form_multiselect_app)
        self.OPTIONS = ["Option A", "Option B", "Option C", "Option D"]

    def test_form_multiselect_default_state(self):
        """Test form multiselect with no URL parameters"""
        self.at.run()

        assert not self.at.exception
        assert self.at.multiselect[0].value == []
        assert not get_query_params(self.at)

    def test_form_multiselect_url_param(self):
        """Test form multiselect with URL parameters set"""
        set_query_params(self.at, {"form_multi": ["Option A", "Option C"]})
        self.at.run()
        
        assert self.at.multiselect[0].value == ["Option A", "Option C"]
        assert self.at.multiselect[0].indices == [0, 2]

    def test_form_multiselect_interaction_updates_url(self):
        """Test that selections update URL parameters after form submission"""
        self.at.run()
        
        # Make selections
        self.at.multiselect[0].select("Option A")
        self.at.multiselect[0].select("Option C")
        # Submit the form
        self.at.button[0].click().run()
        
        # Verify URL parameters updated after submission
        assert get_query_params(self.at)["form_multi"] == ["Option A", "Option C"]
        
        # Modify selections
        self.at.multiselect[0].unselect("Option A")
        self.at.multiselect[0].select("Option D")
        # Submit again
        self.at.button[0].click().run()
        
        # Verify URL parameters updated
        assert get_query_params(self.at)["form_multi"] == ["Option C", "Option D"]

    def test_form_multiselect_no_url_update_without_submit(self):
        """Test that URL parameters don't update until form is submitted"""
        self.at.run()
        
        # Make selections without submitting
        self.at.multiselect[0].set_value(["Option A", "Option B"]).run()
        
        # Verify URL parameters haven't changed
        assert not get_query_params(self.at)
        
        # Submit the form
        self.at.button[0].click().run()
        
        # Verify URL parameters updated after submission
        assert get_query_params(self.at)["form_multi"] == ["Option A", "Option B"]

    def test_form_multiselect_multiple_changes_before_submit(self):
        """Test that only the final selection state before submission is saved to URL"""
        self.at.run()
        
        # Make various changes
        self.at.multiselect[0].select("Option A")
        self.at.multiselect[0].select("Option B")
        self.at.multiselect[0].unselect("Option A")
        self.at.multiselect[0].select("Option C")
        self.at.multiselect[0].unselect("Option B")
        
        # Submit the form
        self.at.button[0].click().run()
        
        # Verify only final state is in URL
        assert get_query_params(self.at)["form_multi"] == ["Option C"] 