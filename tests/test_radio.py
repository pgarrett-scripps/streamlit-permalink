from streamlit.testing.v1 import AppTest

from .utils import get_query_params, set_query_params


def create_radio_app():
    import streamlit_permalink as stp

    OPTIONS = ["Option A", "Option B", "Option C"]
    stp.radio("Test Radio", options=OPTIONS, url_key="radio")


def create_form_radio_app():
    import streamlit_permalink as stp

    form = stp.form("test_form")
    with form:
        OPTIONS = ["Option A", "Option B", "Option C"]
        radio = form.radio("Form Radio", options=OPTIONS, url_key="form_radio")
        submitted = form.form_submit_button("Submit")


class TestRadio:
    def setup_method(self):
        self.at = AppTest.from_function(create_radio_app)
        self.OPTIONS = ["Option A", "Option B", "Option C"]

    def test_radio_default_state(self):
        """Test radio with no URL parameters"""
        self.at.run()

        assert not self.at.exception

        # Verify radio exists and first option is selected by default
        assert len(self.at.radio) == 1
        assert self.at.radio[0].value == self.OPTIONS[0]
        assert self.at.radio[0].index == 0
        # Verify URL parameters are empty

        assert get_query_params(self.at)
        assert get_query_params(self.at)["radio"] == ["Option A"]  # default value

    def test_radio_url_param(self):
        """Test radio with URL parameter set"""
        # Set initial URL parameter
        set_query_params(self.at, {"radio": "Option B"})
        self.at.run()

        assert get_query_params(self.at)
        assert get_query_params(self.at)["radio"] == ["Option B"]

        # Verify radio reflects URL state
        assert self.at.radio[0].value == "Option B"
        assert self.at.radio[0].index == 1

    def test_radio_interaction_updates_url(self):
        """Test that selecting options updates URL parameters"""
        self.at.run()

        # Initially first option and no URL params
        assert self.at.radio[0].value == self.OPTIONS[0]
        assert get_query_params(self.at)
        assert get_query_params(self.at)["radio"] == ["Option A"]  # default value

        # Select new option
        self.at.radio[0].set_value("Option B").run()

        # Verify URL parameter was updated
        assert get_query_params(self.at)["radio"] == ["Option B"]
        assert self.at.radio[0].value == "Option B"
        assert self.at.radio[0].index == 1

        # Select another option
        self.at.radio[0].set_value("Option C").run()

        # Verify URL parameter was updated
        assert get_query_params(self.at)["radio"] == ["Option C"]
        assert self.at.radio[0].value == "Option C"
        assert self.at.radio[0].index == 2

    def test_radio_invalid_url_param(self):
        """Test radio behavior with invalid option value"""
        set_query_params(self.at, {"radio": "Invalid Option"})
        self.at.run()

        assert self.at.exception

    def test_radio_empty_url_param(self):
        """Test radio behavior with empty URL parameter value"""
        set_query_params(self.at, {"radio": ""})
        self.at.run()

        assert self.at.exception

    def test_radio_multiple_url_values(self):
        """Test radio behavior with multiple URL parameter values"""
        set_query_params(self.at, {"radio": ["Option A", "Option B"]})
        self.at.run()

        assert self.at.exception


class TestFormRadio:
    def setup_method(self):
        self.at = AppTest.from_function(create_form_radio_app)
        self.OPTIONS = ["Option A", "Option B", "Option C"]

    def test_form_radio_default_state(self):
        """Test form radio with no URL parameters"""
        self.at.run()

        assert not self.at.exception

        # Verify radio exists and first option is selected by default
        assert len(self.at.radio) == 1
        assert self.at.radio[0].value == self.OPTIONS[0]
        assert self.at.radio[0].index == 0
        # Verify URL parameters are empty
        assert get_query_params(self.at)
        assert get_query_params(self.at)["form_radio"] == ["Option A"]  # default value

    def test_form_radio_url_param(self):
        """Test form radio with URL parameter set"""
        set_query_params(self.at, {"form_radio": "Option B"})
        self.at.run()

        assert get_query_params(self.at)
        assert get_query_params(self.at)["form_radio"] == ["Option B"]

        assert self.at.radio[0].value == "Option B"
        assert self.at.radio[0].index == 1

    def test_form_radio_interaction_updates_url(self):
        """Test that selecting updates URL parameters after form submission"""
        self.at.run()

        # Initially first option and no URL params
        assert self.at.radio[0].value == self.OPTIONS[0]
        assert get_query_params(self.at)
        assert get_query_params(self.at)["form_radio"] == ["Option A"]  # default value
        # Select new option
        self.at.radio[0].set_value("Option B")
        # Submit the form
        self.at.button[0].click().run()

        # Verify URL parameter was updated after form submission
        assert get_query_params(self.at)["form_radio"] == ["Option B"]
        assert self.at.radio[0].value == "Option B"

        # Select another option
        self.at.radio[0].set_value("Option C")
        # Submit the form
        self.at.button[0].click().run()

        # Verify URL parameter was updated after form submission
        assert get_query_params(self.at)["form_radio"] == ["Option C"]
        assert self.at.radio[0].value == "Option C"

    def test_form_radio_no_url_update_without_submit(self):
        """Test that URL parameters don't update until form is submitted"""
        self.at.run()

        # Initially first option and no URL params
        assert self.at.radio[0].value == self.OPTIONS[0]
        assert get_query_params(self.at)
        assert get_query_params(self.at)["form_radio"] == ["Option A"]  # default value

        # Select new option without submitting
        self.at.radio[0].set_value("Option B").run()

        # Verify URL parameters haven't changed
        assert get_query_params(self.at)
        assert get_query_params(self.at)["form_radio"] == ["Option A"]  # default value
        # Now submit the form
        self.at.button[0].click().run()

        # Verify URL parameters updated after submission
        assert get_query_params(self.at)["form_radio"] == ["Option B"]

    def test_form_radio_multiple_changes_before_submit(self):
        """Test that only the final selection before submission is saved to URL"""
        self.at.run()

        # Make multiple selections
        self.at.radio[0].set_value("Option B")
        self.at.radio[0].set_value("Option C")
        self.at.radio[0].set_value("Option A")
        self.at.radio[0].set_value("Option B")

        # Submit the form
        self.at.button[0].click().run()

        # Verify only final selection is in URL
        assert get_query_params(self.at)["form_radio"] == ["Option B"]
        assert self.at.radio[0].value == "Option B"

    def test_form_radio_invalid_url_param(self):
        """Test form radio behavior with invalid option value"""
        set_query_params(self.at, {"form_radio": "Invalid Option"})
        self.at.run()

        assert self.at.exception

    def test_form_radio_empty_url_param(self):
        """Test form radio behavior with empty URL parameter value"""
        set_query_params(self.at, {"form_radio": ""})
        self.at.run()

        assert self.at.exception

    def test_form_radio_multiple_url_values(self):
        """Test form radio behavior with multiple URL parameter values"""
        set_query_params(self.at, {"form_radio": ["Option A", "Option B"]})
        self.at.run()

        assert self.at.exception
