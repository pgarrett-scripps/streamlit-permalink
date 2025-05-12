from streamlit.testing.v1 import AppTest
from datetime import time
from streamlit_permalink import EMPTY_LIST_URL_VALUE, NONE_URL_VALUE

from .utils import get_query_params, set_query_params


def create_time_input_app():
    import streamlit_permalink as stp
    from datetime import time

    # Basic time input with default value
    stp.time_input("Basic Time", value=time(12, 0), url_key="time")

    # Time input with specific value
    stp.time_input("Specific Time", value=time(15, 30, 45), url_key="specific_time")

    # Time input with step
    stp.time_input("Stepped Time", value=time(9, 0), step=3600, url_key="stepped_time")


def create_form_time_input_app():
    import streamlit_permalink as stp
    from datetime import time

    form = stp.form("test_form")
    with form:
        basic_time = form.time_input(
            "Form Time", value=time(12, 0), url_key="form_time"
        )
        stepped_time = form.time_input(
            "Form Stepped Time",
            value=time(9, 0),
            step=3600,
            url_key="form_stepped_time",
        )
        submitted = form.form_submit_button("Submit")


class TestTimeInput:
    def setup_method(self):
        self.at = AppTest.from_function(create_time_input_app)

    def test_time_input_default_state(self):
        """Test time inputs with no URL parameters"""
        self.at.run()

        assert not self.at.exception

        # Verify time inputs exist with correct default values
        assert len(self.at.time_input) == 3
        assert self.at.time_input[0].value == time(12, 0)  # Basic time
        assert self.at.time_input[1].value == time(15, 30, 45)  # Specific time
        assert self.at.time_input[2].value == time(9, 0)  # Stepped time

    def test_time_input_url_params(self):
        """Test time inputs with URL parameters set"""
        # Set initial URL parameters
        set_query_params(
            self.at,
            {"time": "13:45", "specific_time": "16:30", "stepped_time": "10:00"},
        )
        self.at.run()

        # Verify time inputs reflect URL state
        assert self.at.time_input[0].value == time(13, 45)
        assert self.at.time_input[1].value == time(16, 30)
        assert self.at.time_input[2].value == time(10, 0)

    def test_time_input_set_value(self):
        """Test setting specific times"""
        self.at.run()

        # Set new values
        self.at.time_input[0].set_value(time(14, 30)).run()  # ignore seconds

        # Verify URL parameters were updated
        params = get_query_params(self.at)
        assert params["time"] == ["14:30"]
        assert self.at.time_input[0].value == time(14, 30)

    def test_time_input_increment(self):
        """Test increment behavior"""
        self.at.run()

        # Test basic increment (15 minute default step)
        initial_time = self.at.time_input[0].value
        self.at.time_input[0].increment().run()

        # Time should increment by 15 minutes by default
        expected_time = time(
            (initial_time.hour + ((initial_time.minute + 15) // 60)) % 24,
            (initial_time.minute + 15) % 60,
        )
        assert self.at.time_input[0].value == expected_time

        # Test stepped increment (3600 seconds = 1 hour)
        initial_stepped = self.at.time_input[2].value
        self.at.time_input[2].increment().run()
        expected_stepped = time((initial_stepped.hour + 1) % 24, initial_stepped.minute)
        assert self.at.time_input[2].value == expected_stepped

    def test_time_input_decrement(self):
        """Test decrement behavior"""
        self.at.run()

        # Test basic decrement (15 minute default step)
        initial_time = self.at.time_input[0].value
        self.at.time_input[0].decrement().run()

        # Time should decrement by 15 minutes by default
        expected_time = time(
            (initial_time.hour + ((initial_time.minute - 15) // 60)) % 24,
            (initial_time.minute - 15) % 60,
        )
        assert self.at.time_input[0].value == expected_time

        # Test stepped decrement (3600 seconds = 1 hour)
        initial_stepped = self.at.time_input[2].value
        self.at.time_input[2].decrement().run()
        expected_stepped = time((initial_stepped.hour - 1) % 24, initial_stepped.minute)
        assert self.at.time_input[2].value == expected_stepped

    def test_time_input_with_empty_none_values(self):
        """Test time inputs with _EMPTY and _NONE URL parameter values"""
        # Set URL parameters with special values
        set_query_params(
            self.at,
            {
                "time": EMPTY_LIST_URL_VALUE,
                "specific_time": NONE_URL_VALUE,
                "stepped_time": "10:00",
            },
        )

        self.at.run()

        assert self.at.exception

    def test_time_input_invalid_format(self):
        """Test time inputs with invalid format in URL parameters"""
        # Set URL parameters with invalid time format
        set_query_params(
            self.at,
            {
                "time": "13:45",
                "specific_time": "16:30:45",  # Invalid - includes seconds
                "stepped_time": "10:00",
            },
        )

        self.at.run()

        assert self.at.exception

        # Try different invalid format
        set_query_params(
            self.at,
            {
                "time": "13-45",  # Invalid format
                "specific_time": "16:30",
                "stepped_time": "10:00",
            },
        )

        self.at.run()

        assert self.at.exception

    def test_time_input_multiple_values(self):
        """Test time inputs with multiple values in URL parameters"""
        # Set URL parameters with multiple values for a time input
        self.at.query_params["time"] = ["13:45", "14:30"]

        self.at.run()

        assert self.at.exception


class TestFormTimeInput:
    def setup_method(self):
        self.at = AppTest.from_function(create_form_time_input_app)

    def test_form_time_input_default_state(self):
        """Test form time inputs with no URL parameters"""
        self.at.run()

        assert not self.at.exception

        # Verify time inputs exist with default values
        assert len(self.at.time_input) == 2
        assert self.at.time_input[0].value == time(12, 0)
        assert self.at.time_input[1].value == time(9, 0)

        assert get_query_params(self.at)
        assert get_query_params(self.at)["form_time"] == ["12:00"]
        assert get_query_params(self.at)["form_stepped_time"] == ["09:00"]

    def test_form_time_input_url_params(self):
        """Test form time inputs with URL parameters set"""
        set_query_params(self.at, {"form_time": "14:30", "form_stepped_time": "10:00"})
        self.at.run()

        assert self.at.time_input[0].value == time(14, 30)
        assert self.at.time_input[1].value == time(10, 0)

    def test_form_time_input_interaction_updates_url(self):
        """Test that changing times updates URL parameters after form submission"""
        self.at.run()

        # Change times
        self.at.time_input[0].set_value(time(15, 45))
        self.at.time_input[1].increment()  # Should add 1 hour
        # Submit the form
        self.at.button[0].click().run()

        # Verify URL parameters were updated after submission
        params = get_query_params(self.at)
        assert params["form_time"] == ["15:45"]
        assert params["form_stepped_time"] == ["10:00"]

        # Change times again
        self.at.time_input[0].set_value(time(16, 30))
        self.at.time_input[1].decrement()  # Should subtract 1 hour
        # Submit again
        self.at.button[0].click().run()

        # Verify URL parameters were updated
        params = get_query_params(self.at)
        assert params["form_time"] == ["16:30"]
        assert params["form_stepped_time"] == ["09:00"]

    def test_form_time_input_no_url_update_without_submit(self):
        """Test that URL parameters don't update until form is submitted"""
        self.at.run()

        # Change times without submitting
        self.at.time_input[0].set_value(time(17, 15))
        self.at.time_input[1].increment().run()

        assert get_query_params(self.at)
        assert get_query_params(self.at)["form_time"] == ["12:00"]
        assert get_query_params(self.at)["form_stepped_time"] == ["09:00"]

        # Submit the form
        self.at.button[0].click().run()

        # Verify URL parameters updated after submission
        params = get_query_params(self.at)
        assert params["form_time"] == ["17:15"]
        assert params["form_stepped_time"] == ["10:00"]

    def test_form_time_input_multiple_changes_before_submit(self):
        """Test that only the final times before submission are saved to URL"""
        self.at.run()

        # Make multiple changes to times
        self.at.time_input[0].set_value(time(8, 0))
        self.at.time_input[0].increment()
        self.at.time_input[0].set_value(time(9, 30))
        self.at.time_input[1].increment()
        self.at.time_input[1].increment()
        self.at.time_input[1].decrement()

        # Submit the form
        self.at.button[0].click().run()

        # Verify only final times are in URL
        params = get_query_params(self.at)
        assert params["form_time"] == ["09:30"]
        assert params["form_stepped_time"] == ["10:00"]

    def test_form_time_input_with_empty_none_values(self):
        """Test form time inputs with _EMPTY and _NONE URL parameter values"""
        # Set URL parameters with special values
        set_query_params(
            self.at, {"form_time": NONE_URL_VALUE, "form_stepped_time": NONE_URL_VALUE}
        )
        self.at.run()

        assert self.at.exception

    def test_form_time_input_invalid_format(self):
        """Test form time inputs with invalid format in URL parameters"""
        # Set URL parameters with invalid time format
        set_query_params(
            self.at,
            {
                "form_time": "13:45:30",  # Invalid - includes seconds
                "form_stepped_time": "10:00",
            },
        )

        self.at.run()

        assert self.at.exception

        # Try different invalid format
        set_query_params(
            self.at,
            {"form_time": "25:45", "form_stepped_time": "10:00"},  # Invalid hour
        )

        self.at.run()

        assert self.at.exception

    def test_form_time_input_multiple_values(self):
        """Test form time inputs with multiple values in URL parameters"""
        # Set URL parameters with multiple values for a time input
        self.at.query_params["form_time"] = ["13:45", "14:30"]

        self.at.run()

        assert self.at.exception
