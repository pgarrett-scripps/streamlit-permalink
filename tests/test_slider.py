from streamlit.testing.v1 import AppTest
from datetime import datetime, date, time, timedelta

from .utils import get_query_params, set_query_params


def create_single_slider_app():
    import streamlit_permalink as stp

    stp.slider(
        "Single Value Slider", min_value=0, max_value=100, value=50, url_key="slider"
    )


def create_range_slider_app():
    import streamlit_permalink as stp

    stp.slider(
        "Range Slider",
        min_value=0,
        max_value=100,
        value=(25, 75),
        url_key="range_slider",
    )


def create_datetime_slider_app():
    import streamlit_permalink as stp
    from datetime import datetime, timedelta

    start_date = datetime(2024, 1, 1)
    end_date = datetime(2024, 12, 31)
    stp.slider(
        "Datetime Slider",
        min_value=start_date,
        max_value=end_date,
        value=start_date + timedelta(days=180),
        url_key="datetime_slider",
    )


def create_date_slider_app():
    import streamlit_permalink as stp
    from datetime import date

    start_date = date(2024, 1, 1)
    end_date = date(2024, 12, 31)
    stp.slider(
        "Date Slider",
        min_value=start_date,
        max_value=end_date,
        value=start_date,
        url_key="date_slider",
    )


def create_time_slider_app():
    import streamlit_permalink as stp
    from datetime import time

    stp.slider(
        "Time Slider",
        min_value=time(0, 0),
        max_value=time(23, 59),
        value=time(12, 0),
        url_key="time_slider",
    )


def create_form_slider_app():
    import streamlit_permalink as stp

    form = stp.form("test_form")
    with form:
        single = form.slider(
            "Form Single Slider",
            min_value=0,
            max_value=100,
            value=50,
            url_key="form_slider",
        )
        range_slider = form.slider(
            "Form Range Slider",
            min_value=0,
            max_value=100,
            value=(25, 75),
            url_key="form_range",
        )
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
        # Verify URL parameters are set to default
        assert get_query_params(self.at)["slider"] == ["50"]

    def test_slider_url_param(self):
        """Test slider with URL parameter set"""
        # Set initial URL parameter
        set_query_params(self.at, {"slider": ["75"]})
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

    def test_slider_invalid_url_param(self):
        """Test slider behavior with invalid URL parameter value"""
        set_query_params(self.at, {"slider": ["invalid"]})
        self.at.run()

        assert self.at.exception

    def test_slider_out_of_range_above(self):
        """Test slider with out-of-range values"""
        # Test value above max
        set_query_params(self.at, {"slider": ["150"]})
        self.at.run()

        assert self.at.exception

    def test_slider_out_of_range_below(self):
        """Test slider with out-of-range values"""

        # Test value below min
        set_query_params(self.at, {"slider": ["-50"]})
        self.at.run()
        assert self.at.exception

    def test_slider_step(self):
        """Test slider with step parameter"""

        def step_slider_app():
            import streamlit_permalink as stp

            stp.slider(
                "Step Slider",
                min_value=0,
                max_value=10,
                value=2,
                step=2,
                url_key="step_slider",
            )

        at = AppTest.from_function(step_slider_app)
        at.run()

        # Test valid step value
        at.slider[0].set_value(4).run()
        assert get_query_params(at)["step_slider"] == ["4"]

        # Test invalid step value
        set_query_params(at, {"step_slider": ["3"]})
        at.run()

        # assert at.exception (Should probably raise an error, but streamlit doesnt check if value is a multiple of step)


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
        # Verify URL parameters are set to default
        assert get_query_params(self.at)["range_slider"] == ["25", "75"]

    def test_range_slider_url_param(self):
        """Test range slider with URL parameters set"""
        set_query_params(self.at, {"range_slider": ["30", "80"]})
        self.at.run()

        assert self.at.slider[0].value == (30, 80)

    def test_range_slider_interaction_updates_url(self):
        """Test that moving range slider updates URL parameters"""
        self.at.run()

        # Move range slider to new values
        self.at.slider[0].set_range(40, 60).run()

        # Verify URL parameters were updated
        assert get_query_params(self.at)["range_slider"] == ["40", "60"]
        assert self.at.slider[0].value == (40, 60)

    def test_range_slider_invalid_params(self):
        """Test range slider with invalid parameters"""
        # Test invalid number format
        set_query_params(self.at, {"range_slider": ["invalid", "80"]})
        self.at.run()
        assert self.at.exception

        # Test wrong number of values
        set_query_params(self.at, {"range_slider": ["30"]})
        self.at.run()
        assert self.at.exception

        # Test out of order values
        set_query_params(self.at, {"range_slider": ["80", "30"]})
        self.at.run()
        assert self.at.exception

    def test_range_slider_out_of_range(self):
        """Test range slider with out-of-range values"""
        set_query_params(self.at, {"range_slider": ["30", "150"]})
        self.at.run()
        assert self.at.exception

        set_query_params(self.at, {"range_slider": ["-50", "80"]})
        self.at.run()
        assert self.at.exception


class TestDatetimeSlider:
    def setup_method(self):
        self.at = AppTest.from_function(create_datetime_slider_app)
        self.default_date = datetime(2024, 1, 1) + timedelta(days=180)

    def test_datetime_slider_default_state(self):
        """Test datetime slider with no URL parameters"""
        self.at.run()

        assert not self.at.exception
        assert isinstance(self.at.slider[0].value, datetime)
        assert get_query_params(self.at)["datetime_slider"] == [
            self.default_date.strftime("%Y-%m-%dT%H:%M:%S")
        ]

    def test_datetime_slider_url_param(self):
        """Test datetime slider with URL parameter set"""
        test_date = "2024-06-15T12:00:00"
        set_query_params(self.at, {"datetime_slider": [test_date]})
        self.at.run()

        assert not self.at.exception
        assert self.at.slider[0].value == datetime(2024, 6, 15, 12)

    def test_datetime_slider_invalid_format(self):
        """Test datetime slider with invalid datetime format"""
        set_query_params(self.at, {"datetime_slider": ["invalid_date"]})
        self.at.run()
        assert self.at.exception

    def test_datetime_slider_out_of_range(self):
        """Test datetime slider with out-of-range values"""
        set_query_params(self.at, {"datetime_slider": ["2025-01-01 00:00:00"]})
        self.at.run()
        assert self.at.exception


class TestDateSlider:
    def setup_method(self):
        self.at = AppTest.from_function(create_date_slider_app)
        self.default_date = date(2024, 1, 1)

    def test_date_slider_default_state(self):
        """Test date slider with no URL parameters"""
        self.at.run()
        assert not self.at.exception
        assert isinstance(self.at.slider[0].value, date)
        assert get_query_params(self.at)
        assert get_query_params(self.at)["date_slider"] == [
            self.default_date.strftime("%Y-%m-%d")
        ]

    def test_date_slider_url_param(self):
        """Test date slider with URL parameter set"""
        set_query_params(self.at, {"date_slider": ["2024-06-15"]})
        self.at.run()
        assert self.at.slider[0].value == date(2024, 6, 15)

    def test_date_slider_invalid_format(self):
        """Test date slider with invalid date format"""
        set_query_params(self.at, {"date_slider": ["invalid_date"]})
        self.at.run()
        assert self.at.exception


class TestTimeSlider:
    def setup_method(self):
        self.at = AppTest.from_function(create_time_slider_app)
        self.default_time = time(12, 0)

    def test_time_slider_default_state(self):
        """Test time slider with no URL parameters"""
        self.at.run()
        assert not self.at.exception
        assert isinstance(self.at.slider[0].value, time)
        assert get_query_params(self.at)
        assert get_query_params(self.at)["time_slider"] == [
            self.default_time.strftime("%H:%M")
        ]

    def test_time_slider_url_param(self):
        """Test time slider with URL parameter set"""
        set_query_params(self.at, {"time_slider": ["14:30"]})
        self.at.run()
        assert self.at.slider[0].value == time(14, 30)

    def test_time_slider_invalid_format(self):
        """Test time slider with invalid time format"""
        set_query_params(self.at, {"time_slider": ["invalid_time"]})
        self.at.run()
        assert self.at.exception

    def test_time_slider_out_of_range(self):
        """Test time slider with out-of-range values"""
        set_query_params(self.at, {"time_slider": ["24:00"]})
        self.at.run()
        assert self.at.exception


class TestFormSlider:
    def setup_method(self):
        self.at = AppTest.from_function(create_form_slider_app)

    def test_form_sliders_default_state(self):
        """Test form sliders with no URL parameters"""
        self.at.run()

        assert not self.at.exception

        # Verify sliders exist with default values
        assert len(self.at.slider) == 2
        assert self.at.slider[0].value == 50
        assert self.at.slider[1].value == (25, 75)
        # Verify URL parameters are set to default
        assert get_query_params(self.at)["form_slider"] == ["50"]
        assert get_query_params(self.at)["form_range"] == ["25", "75"]

    def test_form_slider_interaction_updates_url(self):
        """Test that moving sliders updates URL parameters after form submission"""
        self.at.run()

        # Move sliders without submitting
        self.at.slider[0].set_value(75).run()
        self.at.slider[1].set_range(40, 60).run()

        # Verify URL hasn't changed before submission
        assert get_query_params(self.at)["form_slider"] == ["50"]
        assert get_query_params(self.at)["form_range"] == ["25", "75"]

        # Submit form
        self.at.button[0].click().run()

        # Verify URL updated after submission
        assert get_query_params(self.at)["form_slider"] == ["75"]
        assert get_query_params(self.at)["form_range"] == ["40", "60"]

    def test_form_slider_multiple_changes_before_submit(self):
        """Test that only final slider positions before submission are saved to URL"""
        self.at.run()

        # Make multiple changes
        self.at.slider[0].set_value(20).run()
        self.at.slider[0].set_value(30).run()
        self.at.slider[1].set_range(10, 90).run()
        self.at.slider[1].set_range(20, 80).run()

        # Submit form
        self.at.button[0].click().run()

        # Verify only final values are in URL
        assert get_query_params(self.at)["form_slider"] == ["30"]
        assert get_query_params(self.at)["form_range"] == ["20", "80"]

    def test_form_slider_invalid_input(self):
        """Test form sliders with invalid input"""
        set_query_params(
            self.at, {"form_slider": "invalid", "form_range": ["20", "invalid"]}
        )
        self.at.run()
        assert self.at.exception

    def test_form_slider_float_values(self):
        """Test form sliders with float values"""

        def float_slider_app():
            import streamlit_permalink as stp

            form = stp.form("test_form")
            with form:
                slider = form.slider(
                    "Float Slider",
                    min_value=0.0,
                    max_value=1.0,
                    value=0.5,
                    step=0.1,
                    url_key="float_slider",
                )
                submitted = form.form_submit_button("Submit")

        at = AppTest.from_function(float_slider_app)
        at.run()

        # Test valid float value
        at.slider[0].set_value(0.7)
        at.button[0].click().run()
        assert get_query_params(at)["float_slider"] == ["0.7"]

        # Test invalid float value
        set_query_params(at, {"float_slider": "1.5"})
        at.run()
        assert at.exception

    def test_form_slider_all_types(self):
        """Test form with different slider types"""

        def multi_type_form_app():
            import streamlit_permalink as stp
            from datetime import date

            form = stp.form("test_form")
            with form:
                int_slider = form.slider("Int Slider", 0, 100, 50, url_key="int_slider")
                float_slider = form.slider(
                    "Float Slider", 0.0, 1.0, 0.5, url_key="float_slider"
                )
                date_slider = form.slider(
                    "Date Slider",
                    date(2024, 1, 1),
                    date(2024, 12, 31),
                    date(2024, 6, 15),
                    url_key="date_slider",
                )
                submitted = form.form_submit_button("Submit")

        at = AppTest.from_function(multi_type_form_app)
        at.run()

        # Set values and submit
        at.slider[0].set_value(75)
        at.slider[1].set_value(0.7)
        at.slider[2].set_value(date(2024, 8, 1))
        at.button[0].click().run()

        params = get_query_params(at)
        assert params["int_slider"] == ["75"]
        assert params["float_slider"] == ["0.7"]
        assert params["date_slider"] == ["2024-08-01"]
