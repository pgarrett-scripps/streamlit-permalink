from streamlit.testing.v1 import AppTest
from packaging.version import parse as V
import streamlit as st
import pytest
from datetime import date
from .utils import get_query_params, set_query_params

def create_date_input_app():
    import streamlit as st
    import streamlit_permalink as stp
    from datetime import date

    # Basic date input with default value
    stp.date_input("Basic Date", value=date(2024, 1, 1), url_key="date")
    
    # Date input with min/max dates
    stp.date_input("Limited Date", 
                   min_value=date(2024, 1, 1),
                   max_value=date(2024, 12, 31),
                   value=date(2024, 6, 15),
                   url_key="limited_date")
    
    # Date range input
    stp.date_input("Date Range",
                   value=(date(2024, 1, 1), date(2024, 12, 31)),
                   url_key="date_range")

def create_form_date_input_app():
    import streamlit as st
    import streamlit_permalink as stp
    from datetime import date

    form = stp.form("test_form")
    with form:
        basic_date = form.date_input("Form Date", 
                                    value=date(2024, 1, 1),
                                    url_key="form_date")
        date_range = form.date_input("Form Date Range",
                                    value=(date(2024, 1, 1), date(2024, 12, 31)),
                                    url_key="form_date_range")
        submitted = form.form_submit_button("Submit")

class TestDateInput:
    def setup_method(self):
        self.at = AppTest.from_function(create_date_input_app)

    def test_date_input_default_state(self):
        """Test date inputs with no URL parameters"""
        self.at.run()

        assert not self.at.exception
        
        # Verify date inputs exist with correct default values
        assert len(self.at.date_input) == 3
        assert self.at.date_input[0].value == date(2024, 1, 1)  # Basic date
        assert self.at.date_input[1].value == date(2024, 6, 15)  # Limited date
        assert self.at.date_input[2].value == (date(2024, 1, 1), date(2024, 12, 31))  # Date range
        # Verify URL parameters are empty
        assert not get_query_params(self.at)

    def test_date_input_url_params(self):
        """Test date inputs with URL parameters set"""
        # Set initial URL parameters
        set_query_params(self.at, {
            "date": "2024-02-15",
            "limited_date": "2024-07-01",
            "date_range": ["2024-03-01", "2024-09-30"]
        })
        self.at.run()
        
        # Verify date inputs reflect URL state
        assert self.at.date_input[0].value == date(2024, 2, 15)
        assert self.at.date_input[1].value == date(2024, 7, 1)
        assert self.at.date_input[2].value == (date(2024, 3, 1), date(2024, 9, 30))

    def test_date_input_set_value(self):
        """Test setting specific dates"""
        self.at.run()
        
        # Set new values
        self.at.date_input[0].set_value(date(2024, 3, 15)).run()
        
        # Verify URL parameters were updated
        params = get_query_params(self.at)
        assert params["date"] == ["2024-03-15"]
        assert self.at.date_input[0].value == date(2024, 3, 15)

    def test_date_input_range_set_value(self):
        """Test setting date range values"""
        self.at.run()
        
        # Set new range values
        new_range = (date(2024, 4, 1), date(2024, 4, 30))
        self.at.date_input[2].set_value(new_range).run()
        
        # Verify URL parameters were updated
        params = get_query_params(self.at)
        assert params["date_range"] == ["2024-04-01", "2024-04-30"]
        assert self.at.date_input[2].value == new_range

    def test_date_input_limits(self):
        """Test that min/max date limits are enforced"""
        # TODO: Implement this, seems buggy
        pass

class TestFormDateInput:
    def setup_method(self):
        self.at = AppTest.from_function(create_form_date_input_app)

    def test_form_date_input_default_state(self):
        """Test form date inputs with no URL parameters"""
        self.at.run()

        assert not self.at.exception
        
        # Verify date inputs exist with default values
        assert len(self.at.date_input) == 2
        assert self.at.date_input[0].value == date(2024, 1, 1)
        assert self.at.date_input[1].value == (date(2024, 1, 1), date(2024, 12, 31))
        # Verify URL parameters are empty
        assert not get_query_params(self.at)

    def test_form_date_input_url_params(self):
        """Test form date inputs with URL parameters set"""
        set_query_params(self.at, {
            "form_date": "2024-03-15",
            "form_date_range": ["2024-06-01", "2024-06-30"]
        })
        self.at.run()
        
        assert self.at.date_input[0].value == date(2024, 3, 15)
        assert self.at.date_input[1].value == (date(2024, 6, 1), date(2024, 6, 30))

    def test_form_date_input_interaction_updates_url(self):
        """Test that changing dates updates URL parameters after form submission"""
        self.at.run()
        
        # Change dates
        self.at.date_input[0].set_value(date(2024, 5, 1))
        self.at.date_input[1].set_value((date(2024, 7, 1), date(2024, 7, 31)))
        # Submit the form
        self.at.button[0].click().run()
        
        # Verify URL parameters were updated after submission
        params = get_query_params(self.at)
        assert params["form_date"] == ["2024-05-01"]
        assert params["form_date_range"] == ["2024-07-01", "2024-07-31"]
        
        # Change dates again
        self.at.date_input[0].set_value(date(2024, 8, 15))
        self.at.date_input[1].set_value((date(2024, 9, 1), date(2024, 9, 30)))
        # Submit again
        self.at.button[0].click().run()
        
        # Verify URL parameters were updated
        params = get_query_params(self.at)
        assert params["form_date"] == ["2024-08-15"]
        assert params["form_date_range"] == ["2024-09-01", "2024-09-30"]

    def test_form_date_input_no_url_update_without_submit(self):
        """Test that URL parameters don't update until form is submitted"""
        self.at.run()
        
        # Change dates without submitting
        self.at.date_input[0].set_value(date(2024, 10, 1))
        self.at.date_input[1].set_value((date(2024, 11, 1), date(2024, 11, 30))).run()
        
        # Verify URL parameters haven't changed
        assert not get_query_params(self.at)
        
        # Submit the form
        self.at.button[0].click().run()
        
        # Verify URL parameters updated after submission
        params = get_query_params(self.at)
        assert params["form_date"] == ["2024-10-01"]
        assert params["form_date_range"] == ["2024-11-01", "2024-11-30"]

    def test_form_date_input_multiple_changes_before_submit(self):
        """Test that only the final dates before submission are saved to URL"""
        self.at.run()
        
        # Make multiple changes to dates
        self.at.date_input[0].set_value(date(2024, 2, 1))
        self.at.date_input[0].set_value(date(2024, 3, 1))
        self.at.date_input[0].set_value(date(2024, 4, 1))
        self.at.date_input[1].set_value((date(2024, 5, 1), date(2024, 5, 31)))
        self.at.date_input[1].set_value((date(2024, 6, 1), date(2024, 6, 30)))
        self.at.date_input[1].set_value((date(2024, 7, 1), date(2024, 7, 31)))
        
        # Submit the form
        self.at.button[0].click().run()
        
        # Verify only final dates are in URL
        params = get_query_params(self.at)
        assert params["form_date"] == ["2024-04-01"]
        assert params["form_date_range"] == ["2024-07-01", "2024-07-31"] 