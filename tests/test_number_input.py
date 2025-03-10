from streamlit.testing.v1 import AppTest
from packaging.version import parse as V
import streamlit as st
import pytest
from .utils import get_query_params, set_query_params

def create_number_input_app():
    import streamlit as st
    import streamlit_permalink as stp

    stp.number_input("Basic Number", value=5, url_key="num")
    stp.number_input("Float Number", value=3.14, step=0.01, url_key="float")
    stp.number_input("Limited Number", min_value=0, max_value=10, value=5, url_key="limited")
    stp.number_input("Stepped Number", value=0, step=5, url_key="stepped")

def create_form_number_input_app():
    import streamlit as st
    import streamlit_permalink as stp

    form = stp.form("test_form")
    with form:
        num = form.number_input("Form Number", value=5, url_key="form_num")
        limited = form.number_input("Form Limited", min_value=0, max_value=10, value=5, url_key="form_limited")
        submitted = form.form_submit_button("Submit")

class TestNumberInput:
    def setup_method(self):
        self.at = AppTest.from_function(create_number_input_app)

    def test_number_input_default_state(self):
        """Test number inputs with no URL parameters"""
        self.at.run()

        assert not self.at.exception
        
        # Verify number inputs exist with correct default values
        assert len(self.at.number_input) == 4
        assert self.at.number_input[0].value == 5  # Basic number
        assert self.at.number_input[1].value == 3.14  # Float number
        assert self.at.number_input[2].value == 5  # Limited number
        assert self.at.number_input[3].value == 0  # Stepped number
        # Verify URL parameters are empty
        assert not get_query_params(self.at)

    def test_number_input_url_params(self):
        """Test number inputs with URL parameters set"""
        # Set initial URL parameters
        set_query_params(self.at, {
            "num": "10",
            "float": "2.718",
            "limited": "7",
            "stepped": "15"
        })
        self.at.run()
        
        # Verify number inputs reflect URL state
        assert self.at.number_input[0].value == 10
        assert self.at.number_input[1].value == 2.718
        assert self.at.number_input[2].value == 7
        assert self.at.number_input[3].value == 15

    def test_number_input_set_value(self):
        """Test setting specific values"""
        self.at.run()
        
        # Set new values
        self.at.number_input[0].set_value(42).run()
        self.at.number_input[1].set_value(1.618).run()
        
        # Verify URL parameters were updated
        params = get_query_params(self.at)
        assert params["num"] == ["42"]
        assert params["float"] == ["1.618"]

    def test_number_input_increment(self):
        """Test increment button behavior"""
        self.at.run()
        
        # Test basic increment
        initial_value = self.at.number_input[0].value
        self.at.number_input[0].increment().run()
        assert self.at.number_input[0].value == initial_value + 1
        assert get_query_params(self.at)["num"] == [str(initial_value + 1)]
        
        # Test stepped increment
        initial_stepped = self.at.number_input[3].value
        self.at.number_input[3].increment().run()
        assert self.at.number_input[3].value == initial_stepped + 5
        assert get_query_params(self.at)["stepped"] == [str(initial_stepped + 5)]

    def test_number_input_decrement(self):
        """Test decrement button behavior"""
        self.at.run()
        
        # Test basic decrement
        initial_value = self.at.number_input[0].value
        self.at.number_input[0].decrement().run()
        assert self.at.number_input[0].value == initial_value - 1
        assert get_query_params(self.at)["num"] == [str(initial_value - 1)]
        
        # Test stepped decrement
        initial_stepped = self.at.number_input[3].value
        self.at.number_input[3].decrement().run()
        assert self.at.number_input[3].value == initial_stepped - 5
        assert get_query_params(self.at)["stepped"] == [str(initial_stepped - 5)]

    def test_number_input_limits(self):
        """Test that min/max limits are enforced"""
        # TODO: Implement this, seems buggy
        pass

class TestFormNumberInput:
    def setup_method(self):
        self.at = AppTest.from_function(create_form_number_input_app)

    def test_form_number_input_default_state(self):
        """Test form number inputs with no URL parameters"""
        self.at.run()

        assert not self.at.exception
        
        # Verify number inputs exist with default values
        assert len(self.at.number_input) == 2
        assert self.at.number_input[0].value == 5
        assert self.at.number_input[1].value == 5
        # Verify URL parameters are empty
        assert not get_query_params(self.at)

    def test_form_number_input_url_params(self):
        """Test form number inputs with URL parameters set"""
        set_query_params(self.at, {
            "form_num": "42",
            "form_limited": "7"
        })
        self.at.run()
        
        assert self.at.number_input[0].value == 42
        assert self.at.number_input[1].value == 7

    def test_form_number_input_interaction_updates_url(self):
        """Test that changing numbers updates URL parameters after form submission"""
        self.at.run()
        
        # Change numbers
        self.at.number_input[0].set_value(15)
        self.at.number_input[1].increment()
        # Submit the form
        self.at.button[0].click().run()
        
        # Verify URL parameters were updated after submission
        params = get_query_params(self.at)
        assert params["form_num"] == ["15"]
        assert params["form_limited"] == ["6"]
        
        # Change numbers again
        self.at.number_input[0].decrement()
        self.at.number_input[1].set_value(8)
        # Submit again
        self.at.button[0].click().run()
        
        # Verify URL parameters were updated
        params = get_query_params(self.at)
        assert params["form_num"] == ["14"]
        assert params["form_limited"] == ["8"]

    def test_form_number_input_no_url_update_without_submit(self):
        """Test that URL parameters don't update until form is submitted"""
        self.at.run()
        
        # Change numbers without submitting
        self.at.number_input[0].set_value(20)
        self.at.number_input[1].increment().run()
        
        # Verify URL parameters haven't changed
        assert not get_query_params(self.at)
        
        # Submit the form
        self.at.button[0].click().run()
        
        # Verify URL parameters updated after submission
        params = get_query_params(self.at)
        assert params["form_num"] == ["20"]
        assert params["form_limited"] == ["6"]

    def test_form_number_input_multiple_changes_before_submit(self):
        """Test that only the final numbers before submission are saved to URL"""
        self.at.run()
        
        # Make multiple changes to numbers
        self.at.number_input[0].set_value(10)
        self.at.number_input[0].increment()
        self.at.number_input[0].decrement()
        self.at.number_input[1].set_value(7)
        self.at.number_input[1].increment()
        self.at.number_input[1].decrement()
        
        # Submit the form
        self.at.button[0].click().run()
        
        # Verify only final numbers are in URL
        params = get_query_params(self.at)
        assert params["form_num"] == ["10"]
        assert params["form_limited"] == ["7"] 