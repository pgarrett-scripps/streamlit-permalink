from streamlit.testing.v1 import AppTest
from datetime import date, datetime

from streamlit_permalink import EMPTY_LIST_URL_VALUE, NONE_URL_VALUE
from .utils import get_query_params, set_query_params


def create_date_input_app():
    import streamlit_permalink as stp
    import streamlit_permalink as st
    from datetime import date, datetime

    # Basic date input with default value
    stp.date_input("Basic Date", value=date(2024, 1, 1), url_key="date")

    # Date input with min/max dates
    stp.date_input(
        "Limited Date",
        min_value=date(2024, 1, 1),
        max_value=date(2024, 12, 31),
        value=date(2024, 6, 15),
        url_key="limited_date",
    )

    # Date range input
    stp.date_input(
        "Date Range", value=(date(2024, 1, 1), date(2024, 12, 31)), url_key="date_range"
    )

    # Date input with 'today' value
    stp.date_input("Today Date", value="today", url_key="today_date")

    # Date input with datetime object
    stp.date_input(
        "Datetime Input",
        value=datetime(2024, 5, 15, 10, 30, 0),
        url_key="datetime_date",
    )


def create_form_date_input_app():
    import streamlit_permalink as stp
    import streamlit_permalink as st
    from datetime import date

    form = stp.form("test_form")
    with form:
        basic_date = form.date_input(
            "Form Date", value=date(2024, 1, 1), url_key="form_date"
        )
        date_range = form.date_input(
            "Form Date Range",
            value=(date(2024, 1, 1), date(2024, 12, 31)),
            url_key="form_date_range",
        )
        submitted = form.form_submit_button("Submit")


class TestDateInput:
    def setup_method(self):
        self.at = AppTest.from_function(create_date_input_app)

    def test_date_input_default_state(self):
        """Test date inputs with no URL parameters"""
        self.at.run()

        assert not self.at.exception
        # Verify URL parameters are initialized with default values
        params = get_query_params(self.at)
        assert params
        assert params["date"] == ["2024-01-01"]
        assert params["limited_date"] == ["2024-06-15"]
        assert params["date_range"] == ["2024-01-01", "2024-12-31"]
        assert "today_date" in params  # Value will vary by day
        assert params["datetime_date"] == ["2024-05-15"]  # Datetime converted to date

        # Verify date inputs exist with correct default values
        assert len(self.at.date_input) == 5  # Now 5 date inputs
        assert self.at.date_input[0].value == date(2024, 1, 1)  # Basic date
        assert self.at.date_input[1].value == date(2024, 6, 15)  # Limited date
        assert self.at.date_input[2].value == (
            date(2024, 1, 1),
            date(2024, 12, 31),
        )  # Date range
        # Today's date will vary, so just check it's a date
        assert isinstance(self.at.date_input[3].value, date)
        assert self.at.date_input[4].value == date(
            2024, 5, 15
        )  # Datetime converted to date

    def test_date_input_url_params(self):
        """Test date inputs with URL parameters set"""
        # Set initial URL parameters
        set_query_params(
            self.at,
            {
                "date": "2024-02-15",
                "limited_date": "2024-07-01",
                "date_range": ["2024-03-01", "2024-09-30"],
                "today_date": "2024-08-01",
                "datetime_date": "2024-06-15",
            },
        )
        self.at.run()

        assert not self.at.exception

        assert get_query_params(self.at)
        assert get_query_params(self.at)["date"] == ["2024-02-15"]
        assert get_query_params(self.at)["limited_date"] == ["2024-07-01"]
        assert get_query_params(self.at)["date_range"] == ["2024-03-01", "2024-09-30"]
        assert get_query_params(self.at)["today_date"] == ["2024-08-01"]
        assert get_query_params(self.at)["datetime_date"] == ["2024-06-15"]

        # Verify date inputs reflect URL state
        assert self.at.date_input[0].value == date(2024, 2, 15)
        assert self.at.date_input[1].value == date(2024, 7, 1)
        assert self.at.date_input[2].value == (date(2024, 3, 1), date(2024, 9, 30))
        assert self.at.date_input[3].value == date(2024, 8, 1)
        assert self.at.date_input[4].value == date(2024, 6, 15)

    def test_date_input_set_value(self):
        """Test setting specific dates"""
        self.at.run()

        # Set new values
        self.at.date_input[0].set_value(date(2024, 3, 15)).run()

        assert get_query_params(self.at)
        assert get_query_params(self.at)["date"] == ["2024-03-15"]
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
        # Set URL parameter with date outside limits
        set_query_params(
            self.at, {"limited_date": "2023-12-31"}  # Before min_value of 2024-01-01
        )

        # This should raise an exception due to date being before min_value
        self.at.run()
        assert self.at.exception

        # Test with date after max_value
        set_query_params(
            self.at, {"limited_date": "2025-01-01"}  # After max_value of 2024-12-31
        )

        # This should raise an exception due to date being after max_value
        self.at.run()
        assert self.at.exception

        # Test with valid date within limits
        set_query_params(self.at, {"limited_date": "2024-06-01"})  # Within limits
        self.at.run()
        assert not self.at.exception
        assert self.at.date_input[1].value == date(2024, 6, 1)

    def test_date_input_invalid_format(self):
        """Test handling of invalid date formats"""
        # Set URL parameter with invalid date format
        set_query_params(self.at, {"date": "not-a-date"})

        # This should raise an exception due to invalid date format
        self.at.run()
        assert self.at.exception

        # Test with another invalid format
        set_query_params(
            self.at, {"date": "01/01/2024"}  # Wrong format, should be YYYY-MM-DD
        )
        self.at.run()
        assert self.at.exception

    def test_date_range_order_validation(self):
        """Test validation of date range ordering"""
        # Set URL parameter with start date after end date
        set_query_params(
            self.at, {"date_range": ["2024-12-31", "2024-01-01"]}  # Start after end
        )

        # This should raise an exception due to invalid range order
        self.at.run()
        assert self.at.exception

    def test_date_range_empty_handling(self):
        """Test handling of _EMPTY in date ranges"""
        # Test with empty for date range (should be valid)
        set_query_params(
            self.at,
            {"date_range": [EMPTY_LIST_URL_VALUE]},  # Use uppercase to match constant
        )
        self.at.run()
        assert not self.at.exception
        assert self.at.date_input[2].value == ()  # Empty tuple

    def test_date_range_single_date_handling(self):
        """Test handling of date range with only start date (single-value tuple)"""
        # Set URL parameter with only start date for range
        set_query_params(self.at, {"date_range": ["2024-05-15"]})  # Only start date

        self.at.run()
        assert not self.at.exception

        # Verify it's interpreted as a single-value tuple
        assert isinstance(self.at.date_input[2].value, tuple)
        assert len(self.at.date_input[2].value) == 1
        assert self.at.date_input[2].value == (date(2024, 5, 15),)

        # Verify the URL parameter is maintained
        params = get_query_params(self.at)
        assert params["date_range"] == ["2024-05-15"]

        # Test setting a single value programmatically
        self.at.date_input[2].set_value((date(2024, 8, 1),)).run()

        # Verify the new value is correct
        assert self.at.date_input[2].value == (date(2024, 8, 1),)
        assert get_query_params(self.at)["date_range"] == ["2024-08-01"]

    def test_date_input_none_handling(self):
        """Test handling of _NONE in single date inputs (representing None)"""
        # Set URL parameter with _NONE for a single date input
        set_query_params(self.at, {"date": [NONE_URL_VALUE]})  # No date selected

        self.at.run()
        assert not self.at.exception

        # Verify it's interpreted as None
        assert self.at.date_input[0].value is None

        # Verify the URL parameter is maintained
        params = get_query_params(self.at)
        assert params["date"] == [NONE_URL_VALUE]

        # Test setting back to a regular date
        self.at.date_input[0].set_value(date(2024, 3, 1)).run()
        assert self.at.date_input[0].value == date(2024, 3, 1)
        assert get_query_params(self.at)["date"] == ["2024-03-01"]

        # Test setting back to None programmatically
        self.at.date_input[0].set_value(None).run()
        assert self.at.date_input[0].value is None
        assert get_query_params(self.at)["date"] == [NONE_URL_VALUE]

    def test_date_input_direct_value_setting(self):
        """Test setting date values directly in the widget"""
        self.at.run()

        # Set a normal date object
        self.at.date_input[0].set_value(date(2024, 6, 30)).run()
        assert not self.at.exception
        assert self.at.date_input[0].value == date(2024, 6, 30)
        assert get_query_params(self.at)["date"] == ["2024-06-30"]

        # Test with None value (should be allowed for single date input)
        self.at.date_input[0].set_value(None).run()
        assert not self.at.exception
        assert self.at.date_input[0].value is None
        assert get_query_params(self.at)["date"] == [NONE_URL_VALUE]

        # Test with a datetime object (should be converted to date)
        test_datetime = datetime(2024, 8, 15, 12, 30, 0)
        self.at.date_input[0].set_value(test_datetime).run()
        assert not self.at.exception
        assert self.at.date_input[0].value == date(2024, 8, 15)
        assert get_query_params(self.at)["date"] == ["2024-08-15"]

        # For date ranges, test setting different types of tuples
        # Empty tuple
        self.at.date_input[2].set_value(()).run()
        assert not self.at.exception
        assert self.at.date_input[2].value == ()
        assert get_query_params(self.at)["date_range"] == [EMPTY_LIST_URL_VALUE]

        # Single-value tuple
        self.at.date_input[2].set_value((date(2024, 9, 1),)).run()
        assert not self.at.exception
        assert self.at.date_input[2].value == (date(2024, 9, 1),)
        assert get_query_params(self.at)["date_range"] == ["2024-09-01"]

        # Two-value tuple
        self.at.date_input[2].set_value((date(2024, 10, 1), date(2024, 10, 31))).run()
        assert not self.at.exception
        assert self.at.date_input[2].value == (date(2024, 10, 1), date(2024, 10, 31))
        assert get_query_params(self.at)["date_range"] == ["2024-10-01", "2024-10-31"]


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

        # Check that URL parameters exist (but don't verify specific values)
        params = get_query_params(self.at)
        assert "form_date" in params
        assert params["form_date"] == ["2024-01-01"]
        assert "form_date_range" in params
        assert params["form_date_range"] == ["2024-01-01", "2024-12-31"]

    def test_form_date_input_url_params(self):
        """Test form date inputs with URL parameters set"""
        set_query_params(
            self.at,
            {
                "form_date": "2024-03-15",
                "form_date_range": ["2024-06-01", "2024-06-30"],
            },
        )
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
        assert "form_date" in params
        assert "form_date_range" in params
        assert params["form_date"] == ["2024-05-01"]
        assert params["form_date_range"] == ["2024-07-01", "2024-07-31"]

        # Change dates again
        self.at.date_input[0].set_value(date(2024, 8, 15))
        self.at.date_input[1].set_value((date(2024, 9, 1), date(2024, 9, 30)))
        # Submit again
        self.at.button[0].click().run()

        # Verify URL parameters were updated
        params = get_query_params(self.at)
        assert "form_date" in params
        assert "form_date_range" in params
        assert params["form_date"] == ["2024-08-15"]
        assert params["form_date_range"] == ["2024-09-01", "2024-09-30"]

        # Change dates as str
        self.at.date_input[0].set_value("2024-08-15").run()
        # Submit again
        self.at.button[0].click().run()

        # Verify URL parameters were updated
        params = get_query_params(self.at)
        assert "form_date" in params
        assert params["form_date"] == ["2024-08-15"]

    def test_form_date_input_no_url_update_without_submit(self):
        """Test that URL parameters don't update until form is submitted"""
        self.at.run()

        # Store initial URL parameters
        initial_params = get_query_params(self.at)

        # Change dates without submitting
        self.at.date_input[0].set_value(date(2024, 10, 1)).run()
        self.at.date_input[1].set_value((date(2024, 11, 1), date(2024, 11, 30))).run()

        # Verify URL parameter values haven't changed from initial
        current_params = get_query_params(self.at)
        assert current_params["form_date"] == initial_params["form_date"]
        assert current_params["form_date_range"] == initial_params["form_date_range"]

        # Submit the form
        self.at.button[0].click().run()

        # Verify URL parameters exist after submission
        final_params = get_query_params(self.at)
        assert "form_date" in final_params
        assert final_params["form_date"] == ["2024-10-01"]
        assert "form_date_range" in final_params
        assert final_params["form_date_range"] == ["2024-11-01", "2024-11-30"]

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

        # Verify final values match what we set
        assert self.at.date_input[0].value == date(2024, 4, 1)
        assert self.at.date_input[1].value == (date(2024, 7, 1), date(2024, 7, 31))
