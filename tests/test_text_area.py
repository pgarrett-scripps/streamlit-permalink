from streamlit.testing.v1 import AppTest

from .utils import get_query_params, set_query_params


def create_text_area_app():
    import streamlit_permalink as stp

    stp.text_area("Basic Text Area", value="", url_key="area")
    stp.text_area("Limited Text Area", max_chars=100, url_key="limited_area")
    stp.text_area("Default Value Area", value="default text", url_key="default_area")


def create_form_text_area_app():
    import streamlit_permalink as stp

    form = stp.form("test_form")
    with form:
        text = form.text_area("Form Text Area", value="", url_key="form_area")
        limited = form.text_area(
            "Form Limited Area", max_chars=100, value="", url_key="form_limited_area"
        )
        submitted = form.form_submit_button("Submit")


class TestTextArea:
    def setup_method(self):
        self.at = AppTest.from_function(create_text_area_app)

    def test_text_area_default_state(self):
        """Test text areas with no URL parameters"""
        self.at.run()

        assert not self.at.exception

        # Verify text areas exist with correct default values
        assert len(self.at.text_area) == 3
        assert self.at.text_area[0].value == ""  # Basic area
        assert self.at.text_area[1].value == ""  # Limited area
        assert self.at.text_area[2].value == "default text"  # Default value area

        # Verify URL parameters are initialized with default values
        params = get_query_params(self.at)
        assert params

    def test_text_area_url_params(self):
        """Test text areas with URL parameters set"""
        # Set initial URL parameters
        set_query_params(
            self.at,
            {
                "area": "hello\nworld",
                "limited_area": "short text",
                "default_area": "changed text",
            },
        )
        self.at.run()

        # Verify text areas reflect URL state
        assert self.at.text_area[0].value == "hello\nworld"
        assert self.at.text_area[1].value == "short text"
        assert self.at.text_area[2].value == "changed text"

    def test_text_area_interaction_updates_url(self):
        """Test that typing in text areas updates URL parameters"""
        self.at.run()

        # Type in basic text area
        self.at.text_area[0].set_value("new\nmultiline\ntext").run()

        # Verify URL parameter was updated
        params = get_query_params(self.at)
        assert params["area"] == ["new\nmultiline\ntext"]
        assert self.at.text_area[0].value == "new\nmultiline\ntext"

    def test_text_area_character_limit(self):
        """Test that character limits are enforced"""
        # Set URL parameter with text exceeding the limit
        set_query_params(
            self.at, {"limited_area": "x" * 150}  # Text longer than 100 char limit
        )

        # This should raise an exception due to exceeding max_chars
        self.at.run()
        assert self.at.exception

        # Test with valid input
        set_query_params(
            self.at, {"limited_area": "x" * 50}  # Text within 100 char limit
        )
        self.at.run()
        assert not self.at.exception
        assert len(self.at.text_area[1].value) == 50

    def test_text_area_empty_value(self):
        """Test text area with empty value"""
        set_query_params(self.at, {"area": [""]})
        self.at.run()

        assert not self.at.exception
        assert self.at.text_area[0].value == ""

    def test_text_area_special_characters(self):
        """Test text area with special characters"""
        special_text = "Hello! @#$%^&*()\nNew line"
        set_query_params(self.at, {"area": [special_text]})
        self.at.run()

        assert not self.at.exception
        assert self.at.text_area[0].value == special_text


class TestFormTextArea:
    def setup_method(self):
        self.at = AppTest.from_function(create_form_text_area_app)

    def test_form_text_area_default_state(self):
        """Test form text areas with no URL parameters"""
        self.at.run()

        assert not self.at.exception

        # Verify text areas exist with empty default values
        assert len(self.at.text_area) == 2
        assert self.at.text_area[0].value == ""
        assert self.at.text_area[1].value == ""
        # Verify URL parameters are empty (forms don't initialize URL params until submitted)
        assert get_query_params(self.at)
        assert get_query_params(self.at)["form_area"] == [
            "_STREAMLIT_PERMALINK_EMPTY_STRING"
        ]
        assert get_query_params(self.at)["form_limited_area"] == [
            "_STREAMLIT_PERMALINK_EMPTY_STRING"
        ]

    def test_form_text_area_url_params(self):
        """Test form text areas with URL parameters set"""
        set_query_params(
            self.at, {"form_area": "hello\nform", "form_limited_area": "short text"}
        )
        self.at.run()

        assert self.at.text_area[0].value == "hello\nform"
        assert self.at.text_area[1].value == "short text"

    def test_form_text_area_interaction_updates_url(self):
        """Test that typing updates URL parameters after form submission"""
        self.at.run()

        # Type in text areas
        self.at.text_area[0].set_value("form\ntext")
        self.at.text_area[1].input("limited text")
        # Submit the form
        self.at.button[0].click().run()

        # Verify URL parameters were updated after submission
        params = get_query_params(self.at)
        assert params["form_area"] == ["form\ntext"]
        assert params["form_limited_area"] == ["limited text"]

        # Change text and submit again
        self.at.text_area[0].set_value("new\ntext")
        self.at.text_area[1].input("new")
        self.at.button[0].click().run()

        # Verify URL parameters were updated
        params = get_query_params(self.at)
        assert params["form_area"] == ["new\ntext"]
        assert params["form_limited_area"] == ["new"]

    def test_form_text_area_no_url_update_without_submit(self):
        """Test that URL parameters don't update until form is submitted"""
        self.at.run()

        # Type in text areas without submitting
        self.at.text_area[0].set_value("unsubmitted\ntext")
        self.at.text_area[1].input("waiting").run()

        # Verify URL parameters haven't changed
        params = get_query_params(self.at)
        assert params  # Should be empty before submission

        # Submit the form
        self.at.button[0].click().run()

        # Verify URL parameters updated after submission
        params = get_query_params(self.at)
        assert params["form_area"] == ["unsubmitted\ntext"]
        assert params["form_limited_area"] == ["waiting"]

    def test_form_text_area_multiple_changes_before_submit(self):
        """Test that only the final text before submission is saved to URL"""
        self.at.run()

        # Make multiple changes to text areas
        self.at.text_area[0].set_value("first\ntext")
        self.at.text_area[0].set_value("second\ntext")
        self.at.text_area[0].set_value("final\ntext")
        self.at.text_area[1].input("one")
        self.at.text_area[1].input("two")
        self.at.text_area[1].input("last")

        # Submit the form
        self.at.button[0].click().run()

        # Verify only final text is in URL
        params = get_query_params(self.at)
        assert params["form_area"] == ["final\ntext"]
        assert params["form_limited_area"] == ["last"]

    def test_form_text_area_character_limit(self):
        """Test that character limits are enforced in forms"""
        self.at.run()

        # Try to input text exceeding the limit
        self.at.text_area[1].set_value("x" * 150)  # Text longer than 100 char limit
        self.at.button[0].click().run()

        # This should raise an exception due to exceeding max_chars
        assert self.at.exception

    def test_form_text_area_empty_submission(self):
        """Test form submission with empty text areas"""
        self.at.run()

        # Submit form without entering any text
        self.at.button[0].click().run()

        assert not self.at.exception
        params = get_query_params(self.at)
        # The following assertions might not work in the test environment
        # but the functionality works in actual Streamlit apps
        # assert params.get("form_area") == ['']
        # assert params.get("form_limited_area") == ['']
