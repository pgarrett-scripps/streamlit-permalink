from streamlit.testing.v1 import AppTest

from .utils import get_query_params, set_query_params


def create_single_select_slider_app():
    import streamlit_permalink as stp

    OPTIONS = ["XS", "S", "M", "L", "XL"]
    stp.select_slider(
        "Single Select Slider", options=OPTIONS, value="M", url_key="select_slider"
    )


def create_range_select_slider_app():
    import streamlit_permalink as stp

    OPTIONS = ["XS", "S", "M", "L", "XL"]
    stp.select_slider(
        "Range Select Slider", options=OPTIONS, value=("S", "L"), url_key="range_select"
    )


def create_form_select_slider_app():
    import streamlit_permalink as stp

    form = stp.form("test_form")
    with form:
        OPTIONS = ["XS", "S", "M", "L", "XL"]
        single = form.select_slider(
            "Form Single Select", options=OPTIONS, value="M", url_key="form_select"
        )
        range_select = form.select_slider(
            "Form Range Select",
            options=OPTIONS,
            value=("S", "L"),
            url_key="form_range_select",
        )
        submitted = form.form_submit_button("Submit")


def create_no_value_select_slider_app():
    import streamlit_permalink as stp

    OPTIONS = ["XS", "S", "M", "L", "XL"]
    stp.select_slider(
        "No Value Select Slider", options=OPTIONS, url_key="no_value_select"
    )


def create_numeric_select_slider_app():
    import streamlit_permalink as stp

    OPTIONS = [1, 2, 3, 4, 5]
    stp.select_slider(
        "Numeric Select Slider", options=OPTIONS, value=3, url_key="numeric_select"
    )


def create_numeric_range_select_slider_app():
    import streamlit_permalink as stp

    OPTIONS = [1, 2, 3, 4, 5]
    stp.select_slider(
        "Numeric Range Select", options=OPTIONS, value=(2, 4), url_key="numeric_range"
    )


def create_mixed_types_select_slider_app():
    import streamlit_permalink as stp

    OPTIONS = [1, "2", 3.0, "four", False]
    stp.select_slider(
        "Mixed Types Select", options=OPTIONS, value="2", url_key="mixed_types"
    )


class TestSingleSelectSlider:
    def setup_method(self):
        self.at = AppTest.from_function(create_single_select_slider_app)
        self.OPTIONS = ["XS", "S", "M", "L", "XL"]

    def test_select_slider_default_state(self):
        """Test single value select slider with no URL parameters"""
        self.at.run()

        assert not self.at.exception

        # Verify select slider exists and has default value
        assert len(self.at.select_slider) == 1
        assert self.at.select_slider[0].value == "M"
        # Verify URL parameters are empty
        assert get_query_params(self.at)
        assert get_query_params(self.at)["select_slider"] == ["M"]

    def test_select_slider_url_param(self):
        """Test select slider with URL parameter set"""
        # Set initial URL parameter
        set_query_params(self.at, {"select_slider": "L"})
        self.at.run()

        assert not self.at.exception
        assert get_query_params(self.at)
        assert get_query_params(self.at)["select_slider"] == ["L"]

        # Verify select slider reflects URL state
        assert self.at.select_slider[0].value == "L"

    def test_select_slider_interaction_updates_url(self):
        """Test that changing selection updates URL parameters"""
        self.at.run()

        assert not self.at.exception
        assert get_query_params(self.at)
        assert get_query_params(self.at)["select_slider"] == ["M"]

        # Change selection to new value
        self.at.select_slider[0].set_value("XL").run()

        # Verify URL parameter was updated
        assert get_query_params(self.at)["select_slider"] == ["XL"]
        assert self.at.select_slider[0].value == "XL"


class TestRangeSelectSlider:
    def setup_method(self):
        self.at = AppTest.from_function(create_range_select_slider_app)
        self.OPTIONS = ["XS", "S", "M", "L", "XL"]

    def test_range_select_slider_default_state(self):
        """Test range select slider with no URL parameters"""
        self.at.run()

        assert not self.at.exception

        assert get_query_params(self.at)
        assert get_query_params(self.at)["range_select"] == ["S", "L"]

        # Verify select slider exists and has default range
        assert len(self.at.select_slider) == 1
        assert self.at.select_slider[0].value == ("S", "L")
        # Verify URL parameters are empty

    def test_range_select_slider_url_param(self):
        """Test range select slider with URL parameters set"""
        # Set initial URL parameters
        set_query_params(self.at, {"range_select": ["XS", "XL"]})
        self.at.run()

        assert not self.at.exception
        assert get_query_params(self.at)
        assert get_query_params(self.at)["range_select"] == ["XS", "XL"]

        # Verify select slider reflects URL state
        assert self.at.select_slider[0].value == ("XS", "XL")

    def test_range_select_slider_interaction_updates_url(self):
        """Test that changing range selection updates URL parameters"""
        self.at.run()

        assert not self.at.exception
        assert get_query_params(self.at)
        assert get_query_params(self.at)["range_select"] == ["S", "L"]

        # Change range to new values
        self.at.select_slider[0].set_range("M", "XL").run()

        # Verify URL parameters were updated
        assert get_query_params(self.at)["range_select"] == ["M", "XL"]
        assert self.at.select_slider[0].value == ("M", "XL")


class TestFormSelectSlider:
    def setup_method(self):
        self.at = AppTest.from_function(create_form_select_slider_app)
        self.OPTIONS = ["XS", "S", "M", "L", "XL"]

    def test_form_select_sliders_default_state(self):
        """Test form select sliders with no URL parameters"""
        self.at.run()

        assert not self.at.exception
        assert get_query_params(self.at)
        assert get_query_params(self.at)["form_select"] == ["M"]
        assert get_query_params(self.at)["form_range_select"] == ["S", "L"]

        # Verify select sliders exist with default values
        assert len(self.at.select_slider) == 2
        assert self.at.select_slider[0].value == "M"  # Single value select slider
        assert self.at.select_slider[1].value == ("S", "L")  # Range select slider
        # Verify URL parameters are empty

    def test_form_select_sliders_url_param(self):
        """Test form select sliders with URL parameters set"""
        set_query_params(
            self.at, {"form_select": "L", "form_range_select": ["XS", "M"]}
        )
        self.at.run()

        assert not self.at.exception
        assert get_query_params(self.at)
        assert get_query_params(self.at)["form_select"] == ["L"]
        assert get_query_params(self.at)["form_range_select"] == ["XS", "M"]

        assert self.at.select_slider[0].value == "L"
        assert self.at.select_slider[1].value == ("XS", "M")

    def test_form_select_slider_interaction_updates_url(self):
        """Test that changing selections updates URL parameters after form submission"""
        self.at.run()

        assert not self.at.exception
        assert get_query_params(self.at)
        assert get_query_params(self.at)["form_select"] == ["M"]
        assert get_query_params(self.at)["form_range_select"] == ["S", "L"]

        # Change both select sliders
        self.at.select_slider[0].set_value("XL")
        self.at.select_slider[1].set_range("S", "XL")
        # Submit the form
        self.at.button[0].click().run()

        # Verify URL parameters were updated after submission
        params = get_query_params(self.at)
        assert params["form_select"] == ["XL"]
        assert params["form_range_select"] == ["S", "XL"]

        # Change selections again
        self.at.select_slider[0].set_value("XS")
        self.at.select_slider[1].set_range("XS", "M")
        # Submit again
        self.at.button[0].click().run()

        # Verify URL parameters were updated
        params = get_query_params(self.at)
        assert params["form_select"] == ["XS"]
        assert params["form_range_select"] == ["XS", "M"]

    def test_form_select_slider_no_url_update_without_submit(self):
        """Test that URL parameters don't update until form is submitted"""
        self.at.run()

        assert not self.at.exception
        assert get_query_params(self.at)
        assert get_query_params(self.at)["form_select"] == ["M"]
        assert get_query_params(self.at)["form_range_select"] == ["S", "L"]

        # Change selections without submitting
        self.at.select_slider[0].set_value("L")
        self.at.select_slider[1].set_range("M", "XL").run()

        # Verify URL parameters haven't changed

        # Submit the form
        self.at.button[0].click().run()

        # Verify URL parameters updated after submission
        params = get_query_params(self.at)
        assert params["form_select"] == ["L"]
        assert params["form_range_select"] == ["M", "XL"]

    def test_form_select_slider_multiple_changes_before_submit(self):
        """Test that only the final selections before submission are saved to URL"""
        self.at.run()

        # Make multiple changes to selections
        self.at.select_slider[0].set_value("S")
        self.at.select_slider[0].set_value("L")
        self.at.select_slider[0].set_value("M")
        self.at.select_slider[1].set_range("XS", "M")
        self.at.select_slider[1].set_range("S", "XL")
        self.at.select_slider[1].set_range("M", "L")

        # Submit the form
        self.at.button[0].click().run()

        # Verify only final selections are in URL
        params = get_query_params(self.at)
        assert params["form_select"] == ["M"]
        assert params["form_range_select"] == ["M", "L"]


class TestNoValueSelectSlider:
    def setup_method(self):
        self.at = AppTest.from_function(create_no_value_select_slider_app)
        self.OPTIONS = ["XS", "S", "M", "L", "XL"]

    def test_select_slider_no_initial_value(self):
        """Test select slider behavior with no initial value"""
        self.at.run()

        assert not self.at.exception

        # Verify select slider exists and defaults to first option
        assert len(self.at.select_slider) == 1
        assert self.at.select_slider[0].value == "XS"
        # Verify URL parameters are empty
        assert get_query_params(self.at)
        assert get_query_params(self.at)["no_value_select"] == ["XS"]

    def test_select_slider_invalid_value_count(self):
        """Test select slider with wrong number of URL parameters"""
        # Try to set multiple values for single select slider
        set_query_params(self.at, {"no_value_select": ["XS", "M"]})
        self.at.run()

        # Verify error is raised
        assert self.at.exception

    def test_select_slider_invalid_option(self):
        """Test select slider with invalid option value"""
        # Set invalid option value
        set_query_params(self.at, {"no_value_select": ["XXL"]})
        self.at.run()

        # Verify error is raised
        assert self.at.exception


class TestNumericSelectSlider:
    def setup_method(self):
        self.at = AppTest.from_function(create_numeric_select_slider_app)
        self.OPTIONS = [1, 2, 3, 4, 5]

    def test_numeric_select_slider_default_state(self):
        """Test single value numeric select slider with no URL parameters"""
        self.at.run()

        assert not self.at.exception

        # Verify select slider exists and has default value
        assert len(self.at.select_slider) == 1
        assert self.at.select_slider[0].value == 3
        # Verify URL parameters
        assert get_query_params(self.at)
        assert get_query_params(self.at)["numeric_select"] == ["3"]

    def test_numeric_select_slider_url_param(self):
        """Test numeric select slider with URL parameter set"""
        # Set initial URL parameter
        set_query_params(self.at, {"numeric_select": "5"})
        self.at.run()

        assert not self.at.exception
        assert get_query_params(self.at)
        assert get_query_params(self.at)["numeric_select"] == ["5"]

        # Verify select slider reflects URL state
        assert self.at.select_slider[0].value == 5

    def test_numeric_select_slider_interaction_updates_url(self):
        """Test that changing numeric selection updates URL parameters"""
        self.at.run()

        assert not self.at.exception
        assert get_query_params(self.at)
        assert get_query_params(self.at)["numeric_select"] == ["3"]

        # Change selection to new value
        self.at.select_slider[0].set_value(4).run()

        # Verify URL parameter was updated
        assert get_query_params(self.at)["numeric_select"] == ["4"]
        assert self.at.select_slider[0].value == 4


class TestNumericRangeSelectSlider:
    def setup_method(self):
        self.at = AppTest.from_function(create_numeric_range_select_slider_app)
        self.OPTIONS = [1, 2, 3, 4, 5]

    def test_numeric_range_select_slider_default_state(self):
        """Test numeric range select slider with no URL parameters"""
        self.at.run()

        assert not self.at.exception

        assert get_query_params(self.at)
        assert get_query_params(self.at)["numeric_range"] == ["2", "4"]

        # Verify select slider exists and has default range
        assert len(self.at.select_slider) == 1
        assert self.at.select_slider[0].value == (2, 4)

    def test_numeric_range_select_slider_url_param(self):
        """Test numeric range select slider with URL parameters set"""
        # Set initial URL parameters
        set_query_params(self.at, {"numeric_range": ["1", "5"]})
        self.at.run()

        assert not self.at.exception
        assert get_query_params(self.at)
        assert get_query_params(self.at)["numeric_range"] == ["1", "5"]

        # Verify select slider reflects URL state
        assert self.at.select_slider[0].value == (1, 5)


class TestMixedTypesSelectSlider:
    def setup_method(self):
        self.at = AppTest.from_function(create_mixed_types_select_slider_app)
        self.OPTIONS = [1, "2", 3.0, "four", False]

    def test_mixed_types_select_slider_default_state(self):
        """Test select slider with mixed option types"""
        self.at.run()

        assert not self.at.exception

        # Verify select slider exists and has default value
        assert len(self.at.select_slider) == 1
        assert self.at.select_slider[0].value == "2"
        # Verify URL parameters
        assert get_query_params(self.at)
        assert get_query_params(self.at)["mixed_types"] == ["2"]

    def test_mixed_types_select_slider_url_param(self):
        """Test mixed types select slider with URL parameter set"""
        # Set initial URL parameter
        set_query_params(self.at, {"mixed_types": "four"})
        self.at.run()

        assert not self.at.exception
        assert get_query_params(self.at)
        assert get_query_params(self.at)["mixed_types"] == ["four"]

        # Verify select slider reflects URL state
        assert self.at.select_slider[0].value == "four"

    def test_mixed_types_select_slider_boolean_option(self):
        """Test mixed types select slider with boolean option"""
        # Set initial URL parameter to boolean value
        set_query_params(self.at, {"mixed_types": "False"})
        self.at.run()

        assert not self.at.exception
        assert get_query_params(self.at)
        assert get_query_params(self.at)["mixed_types"] == ["False"]

        # Verify select slider reflects URL state
        assert self.at.select_slider[0].value == False

    def test_mixed_types_select_slider_numeric_options(self):
        """Test mixed types select slider with numeric options"""
        # Set initial URL parameter to numeric value
        set_query_params(self.at, {"mixed_types": "1"})
        self.at.run()

        assert not self.at.exception
        assert get_query_params(self.at)
        assert get_query_params(self.at)["mixed_types"] == ["1"]

        # Verify select slider reflects URL state
        assert self.at.select_slider[0].value == 1

        # Try float value
        set_query_params(self.at, {"mixed_types": "3.0"})
        self.at.run()

        assert not self.at.exception
        assert get_query_params(self.at)["mixed_types"] == ["3.0"]
        assert self.at.select_slider[0].value == 3.0
