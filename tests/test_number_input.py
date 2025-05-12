from streamlit.testing.v1 import AppTest

from .utils import get_query_params, set_query_params


def create_number_input_app():
    import streamlit_permalink as stp

    stp.number_input("Basic Number", value=5, url_key="num")
    stp.number_input("Float Number", value=3.14, step=0.01, url_key="float")
    stp.number_input(
        "Limited Number", min_value=0, max_value=10, value=5, url_key="limited"
    )
    stp.number_input("Stepped Number", value=0, step=5, url_key="stepped")
    # Add test for "min" default value
    stp.number_input("Min Default", min_value=10, max_value=100, url_key="min_default")
    # Add test for None value
    stp.number_input("None Value", value=None, url_key="none_value")


def create_form_number_input_app():
    import streamlit_permalink as stp

    form = stp.form("test_form")
    with form:
        num = form.number_input("Form Number", value=5, url_key="form_num")
        limited = form.number_input(
            "Form Limited", min_value=0, max_value=10, value=5, url_key="form_limited"
        )
        submitted = form.form_submit_button("Submit")


class TestNumberInput:
    def setup_method(self):
        self.at = AppTest.from_function(create_number_input_app)

    def test_number_input_default_state(self):
        """Test number inputs with no URL parameters"""
        self.at.run()

        assert not self.at.exception

        # Verify number inputs exist with correct default values
        assert len(self.at.number_input) == 6
        assert self.at.number_input[0].value == 5  # Basic number
        assert self.at.number_input[1].value == 3.14  # Float number
        assert self.at.number_input[2].value == 5  # Limited number
        assert self.at.number_input[3].value == 0  # Stepped number
        assert (
            self.at.number_input[4].value == 10
        )  # Min default (should default to min_value)
        assert self.at.number_input[5].value is None  # None value

        # Verify URL parameters are set for initial values
        params = get_query_params(self.at)
        assert params["num"] == ["5"]
        assert params["float"] == ["3.14"]
        assert params["limited"] == ["5"]
        assert params["stepped"] == ["0"]
        assert params["min_default"] == ["10"]
        assert params["none_value"] == ["_STREAMLIT_PERMALINK_NONE"]

    def test_number_input_url_params(self):
        """Test number inputs with URL parameters set"""
        # Set initial URL parameters
        set_query_params(
            self.at,
            {
                "num": "10",
                "float": "2.718",
                "limited": "7",
                "stepped": "15",
                "min_default": "50",
                "none_value": "42",
            },
        )
        self.at.run()

        assert get_query_params(self.at)
        assert get_query_params(self.at)["num"] == ["10"]
        assert get_query_params(self.at)["float"] == ["2.718"]
        assert get_query_params(self.at)["limited"] == ["7"]
        assert get_query_params(self.at)["stepped"] == ["15"]
        assert get_query_params(self.at)["min_default"] == ["50"]
        assert get_query_params(self.at)["none_value"] == ["42"]

        # Verify number inputs reflect URL state
        assert self.at.number_input[0].value == 10
        assert self.at.number_input[1].value == 2.718
        assert self.at.number_input[2].value == 7
        assert self.at.number_input[3].value == 15
        assert self.at.number_input[4].value == 50
        assert self.at.number_input[5].value == 42

    def test_number_input_set_value(self):
        """Test setting specific values"""
        self.at.run()

        assert get_query_params(self.at)
        assert get_query_params(self.at)["num"] == ["5"]
        assert get_query_params(self.at)["float"] == ["3.14"]
        assert get_query_params(self.at)["limited"] == ["5"]
        assert get_query_params(self.at)["stepped"] == ["0"]
        assert get_query_params(self.at)["min_default"] == ["10"]
        assert get_query_params(self.at)["none_value"] == ["_STREAMLIT_PERMALINK_NONE"]

        # Verify number inputs reflect URL state
        assert self.at.number_input[0].value == 5
        assert self.at.number_input[1].value == 3.14
        assert self.at.number_input[2].value == 5
        assert self.at.number_input[3].value == 0
        assert self.at.number_input[4].value == 10
        assert self.at.number_input[5].value == None

        # Set new values
        self.at.number_input[0].set_value(42).run()
        self.at.number_input[1].set_value(1.618).run()

        # Verify URL parameters were updated
        assert get_query_params(self.at)
        assert get_query_params(self.at)["num"] == ["42"]
        assert get_query_params(self.at)["float"] == ["1.618"]
        assert get_query_params(self.at)["limited"] == ["5"]
        assert get_query_params(self.at)["stepped"] == ["0"]
        assert get_query_params(self.at)["min_default"] == ["10"]
        assert get_query_params(self.at)["none_value"] == ["_STREAMLIT_PERMALINK_NONE"]

        # Verify number inputs reflect URL state
        assert self.at.number_input[0].value == 42
        assert self.at.number_input[1].value == 1.618
        assert self.at.number_input[2].value == 5
        assert self.at.number_input[3].value == 0
        assert self.at.number_input[4].value == 10
        assert self.at.number_input[5].value == None

    def test_number_input_increment(self):
        """Test increment button behavior"""
        self.at.run()

        assert get_query_params(self.at)
        assert get_query_params(self.at)["num"] == ["5"]
        assert get_query_params(self.at)["float"] == ["3.14"]
        assert get_query_params(self.at)["limited"] == ["5"]
        assert get_query_params(self.at)["stepped"] == ["0"]
        assert get_query_params(self.at)["min_default"] == ["10"]
        assert get_query_params(self.at)["none_value"] == ["_STREAMLIT_PERMALINK_NONE"]

        # Verify number inputs reflect URL state
        assert self.at.number_input[0].value == 5
        assert self.at.number_input[1].value == 3.14
        assert self.at.number_input[2].value == 5
        assert self.at.number_input[3].value == 0
        assert self.at.number_input[4].value == 10
        assert self.at.number_input[5].value == None

        # Test basic increment
        self.at.number_input[0].increment().run()  # increase by 1 (default step = 1)
        self.at.number_input[
            1
        ].decrement().run()  # decrease by 0.01 (default step = 0.01)
        self.at.number_input[2].decrement().run()  # decrease by 1 (default step = 1)
        self.at.number_input[3].increment().run()  # increase by 5 (step = 5)

        assert get_query_params(self.at)
        assert get_query_params(self.at)["num"] == ["6"]
        assert get_query_params(self.at)["float"] == ["3.1300000000000003"]
        assert get_query_params(self.at)["limited"] == ["4"]
        assert get_query_params(self.at)["stepped"] == ["5"]
        assert get_query_params(self.at)["min_default"] == ["10"]
        assert get_query_params(self.at)["none_value"] == ["_STREAMLIT_PERMALINK_NONE"]

        # Verify number inputs reflect URL state
        assert self.at.number_input[0].value == 6
        assert self.at.number_input[1].value == 3.1300000000000003
        assert self.at.number_input[2].value == 4
        assert self.at.number_input[3].value == 5
        assert self.at.number_input[4].value == 10
        assert self.at.number_input[5].value == None

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

    def test_number_input_limits_min(self):
        """Test that min/max limits are enforced"""
        # Set URL parameters with values outside limits
        set_query_params(
            self.at,
            {
                "limited": "-5",  # Below min_value of 0
            },
        )
        self.at.run()
        assert self.at.exception

    def test_number_input_limits_max(self):
        """Test that max limit is enforced"""
        # Set URL parameters with value above max_value
        set_query_params(
            self.at,
            {
                "limited": "15",  # Above max_value of 10
            },
        )
        self.at.run()
        assert self.at.exception

    def test_number_input_invalid_type(self):
        """Test handling of invalid input types"""
        # Set URL parameter with non-numeric value
        set_query_params(
            self.at,
            {
                "num": "not-a-number",
            },
        )

        self.at.run()
        assert self.at.exception


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

        assert get_query_params(self.at)
        assert get_query_params(self.at)["form_num"] == ["5"]
        assert get_query_params(self.at)["form_limited"] == ["5"]

    def test_form_number_input_url_params(self):
        """Test form number inputs with URL parameters set"""
        set_query_params(self.at, {"form_num": "42", "form_limited": "7"})
        self.at.run()

        assert not self.at.exception
        assert get_query_params(self.at)
        assert get_query_params(self.at)["form_num"] == ["42"]
        assert get_query_params(self.at)["form_limited"] == ["7"]

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
        assert get_query_params(self.at)
        assert get_query_params(self.at)["form_num"] == ["5"]
        assert get_query_params(self.at)["form_limited"] == ["5"]

        # valuesupdated on form but not on url
        assert self.at.number_input[0].value == 20
        assert self.at.number_input[1].value == 6

        # Submit the form
        self.at.button[0].click().run()

        # Verify URL parameters updated after submission
        params = get_query_params(self.at)
        assert params["form_num"] == ["20"]
        assert params["form_limited"] == ["6"]

        assert self.at.number_input[0].value == 20
        assert self.at.number_input[1].value == 6

    def test_form_number_input_multiple_changes_before_submit(self):
        """Test that only the final numbers before submission are saved to URL"""
        self.at.run()

        # Make multiple changes to numbers
        self.at.number_input[0].set_value(10)
        self.at.number_input[0].increment()
        self.at.number_input[0].decrement()
        self.at.number_input[0].decrement()
        self.at.number_input[1].set_value(7)
        self.at.number_input[1].increment()
        self.at.number_input[1].decrement()
        self.at.number_input[1].decrement()

        # Submit the form
        self.at.button[0].click().run()

        # Verify only final numbers are in URL
        params = get_query_params(self.at)
        assert params["form_num"] == ["9"]
        assert params["form_limited"] == ["6"]

        assert self.at.number_input[0].value == 9
        assert self.at.number_input[1].value == 6
