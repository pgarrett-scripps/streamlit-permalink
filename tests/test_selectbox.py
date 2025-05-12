from streamlit.testing.v1 import AppTest

from .utils import get_query_params, set_query_params


def create_selectbox_app():
    import streamlit_permalink as stp

    OPTIONS = ["Option A", "Option B", "Option C"]
    stp.selectbox("Test Selectbox", options=OPTIONS, url_key="select")


def create_form_selectbox_app():
    import streamlit_permalink as stp

    form = stp.form("test_form")
    with form:
        OPTIONS = ["Option A", "Option B", "Option C"]
        selectbox = form.selectbox(
            "Form Selectbox", options=OPTIONS, url_key="form_select"
        )
        submitted = form.form_submit_button("Submit")


class TestSelectbox:
    def setup_method(self):
        self.at = AppTest.from_function(create_selectbox_app)
        self.OPTIONS = ["Option A", "Option B", "Option C"]

    def test_selectbox_default_state(self):
        """Test selectbox with no URL parameters"""
        self.at.run()

        assert not self.at.exception

        # Verify selectbox exists and first option is selected by default
        assert len(self.at.selectbox) == 1
        assert self.at.selectbox[0].value == self.OPTIONS[0]
        assert self.at.selectbox[0].index == 0
        # Verify URL parameters are empty
        assert get_query_params(self.at)
        assert get_query_params(self.at)["select"] == ["Option A"]  # default value

    def test_selectbox_url_param(self):
        """Test selectbox with URL parameter set"""
        # Set initial URL parameter
        set_query_params(self.at, {"select": "Option B"})
        self.at.run()

        assert get_query_params(self.at)
        assert get_query_params(self.at)["select"] == ["Option B"]

        # Verify selectbox reflects URL state
        assert self.at.selectbox[0].value == "Option B"
        assert self.at.selectbox[0].index == 1

    def test_selectbox_interaction_by_value_updates_url(self):
        """Test that selecting options by value updates URL parameters"""
        self.at.run()

        # Initially first option and no URL params
        assert self.at.selectbox[0].value == self.OPTIONS[0]
        assert get_query_params(self.at)
        assert get_query_params(self.at)["select"] == ["Option A"]  # default value
        # Select by value
        self.at.selectbox[0].select("Option B").run()

        # Verify URL parameter was updated
        assert get_query_params(self.at)["select"] == ["Option B"]
        assert self.at.selectbox[0].value == "Option B"
        assert self.at.selectbox[0].index == 1

    def test_selectbox_interaction_by_index_updates_url(self):
        """Test that selecting options by index updates URL parameters"""
        self.at.run()

        # Initially first option and no URL params
        assert self.at.selectbox[0].index == 0
        assert get_query_params(self.at)
        assert get_query_params(self.at)["select"] == ["Option A"]  # default value

        # Select by index
        self.at.selectbox[0].select_index(2).run()

        # Verify URL parameter was updated
        assert get_query_params(self.at)["select"] == ["Option C"]
        assert self.at.selectbox[0].value == "Option C"
        assert self.at.selectbox[0].index == 2

    def test_selectbox_invalid_url_param(self):
        """Test selectbox behavior with invalid option value"""
        set_query_params(self.at, {"select": "Invalid Option"})
        self.at.run()

        assert get_query_params(self.at)
        assert get_query_params(self.at)["select"] == [
            "Invalid Option"
        ]  # default value

        assert self.at.exception

    def test_selectbox_empty_url_param(self):
        """Test selectbox behavior with empty URL parameter value"""
        set_query_params(self.at, {"select": ""})
        self.at.run()

        assert self.at.exception

    def test_selectbox_multiple_url_values(self):
        """Test selectbox behavior with multiple URL parameter values"""
        set_query_params(self.at, {"select": ["Option A", "Option B"]})
        self.at.run()

        assert self.at.exception


class TestFormSelectbox:
    def setup_method(self):
        self.at = AppTest.from_function(create_form_selectbox_app)
        self.OPTIONS = ["Option A", "Option B", "Option C"]

    def test_form_selectbox_default_state(self):
        """Test form selectbox with no URL parameters"""
        self.at.run()

        assert not self.at.exception

        # Verify selectbox exists and first option is selected by default
        assert len(self.at.selectbox) == 1
        assert self.at.selectbox[0].value == self.OPTIONS[0]
        assert self.at.selectbox[0].index == 0
        # Verify URL parameters are empty
        assert get_query_params(self.at)
        assert get_query_params(self.at)["form_select"] == ["Option A"]  # default value

    def test_form_selectbox_url_param(self):
        """Test form selectbox with URL parameter set"""
        set_query_params(self.at, {"form_select": "Option B"})
        self.at.run()

        assert self.at.selectbox[0].value == "Option B"
        assert self.at.selectbox[0].index == 1

    def test_form_selectbox_interaction_updates_url(self):
        """Test that selecting updates URL parameters after form submission"""
        self.at.run()

        # Initially first option and no URL params
        assert self.at.selectbox[0].value == self.OPTIONS[0]
        assert get_query_params(self.at)
        assert get_query_params(self.at)["form_select"] == ["Option A"]  # default value
        # Select new option
        self.at.selectbox[0].select("Option B")
        # Submit the form
        self.at.button[0].click().run()

        # Verify URL parameter was updated after form submission
        assert get_query_params(self.at)["form_select"] == ["Option B"]
        assert self.at.selectbox[0].value == "Option B"

        # Select another option
        self.at.selectbox[0].select_index(2)
        # Submit the form
        self.at.button[0].click().run()

        # Verify URL parameter was updated after form submission
        assert get_query_params(self.at)["form_select"] == ["Option C"]
        assert self.at.selectbox[0].value == "Option C"

    def test_form_selectbox_no_url_update_without_submit(self):
        """Test that URL parameters don't update until form is submitted"""
        self.at.run()

        # Initially first option and no URL params
        assert self.at.selectbox[0].value == self.OPTIONS[0]
        assert get_query_params(self.at)
        assert get_query_params(self.at)["form_select"] == ["Option A"]  # default value

        # Select new option without submitting
        self.at.selectbox[0].select("Option B").run()

        # Verify URL parameters haven't changed
        assert get_query_params(self.at)
        assert get_query_params(self.at)["form_select"] == ["Option A"]  # default value

        # Now submit the form
        self.at.button[0].click().run()

        # Verify URL parameters updated after submission
        assert get_query_params(self.at)
        assert get_query_params(self.at)["form_select"] == ["Option B"]

    def test_form_selectbox_multiple_changes_before_submit(self):
        """Test that only the final selection before submission is saved to URL"""
        self.at.run()

        # Make multiple selections
        self.at.selectbox[0].select("Option B")
        self.at.selectbox[0].select("Option C")
        self.at.selectbox[0].select("Option A")
        self.at.selectbox[0].select("Option B")

        # Submit the form
        self.at.button[0].click().run()

        # Verify only final selection is in URL
        assert get_query_params(self.at)["form_select"] == ["Option B"]
        assert self.at.selectbox[0].value == "Option B"

    def test_form_selectbox_invalid_url_param(self):
        """Test form selectbox behavior with invalid option value"""
        set_query_params(self.at, {"form_select": "Invalid Option"})
        self.at.run()

        assert self.at.exception

    def test_form_selectbox_empty_url_param(self):
        """Test form selectbox behavior with empty URL parameter value"""
        set_query_params(self.at, {"form_select": ""})
        self.at.run()

        assert self.at.exception

    def test_form_selectbox_multiple_url_values(self):
        """Test form selectbox behavior with multiple URL parameter values"""
        set_query_params(self.at, {"form_select": ["Option A", "Option B"]})
        self.at.run()

        assert self.at.exception
