from streamlit.testing.v1 import AppTest
from .utils import get_query_params, set_query_params


def create_checkbox_app():
    import streamlit_permalink as st
    import streamlit_permalink as stp

    stp.checkbox("Test Checkbox", url_key="check")


class TestCheckbox:
    def setup_method(self):
        self.at = AppTest.from_function(create_checkbox_app)

    def test_checkbox_default_state(self):
        """Test checkbox with no URL parameters"""
        self.at.run()

        assert not self.at.exception

        # Verify checkbox exists and is unchecked by default
        assert len(self.at.checkbox) == 1
        assert self.at.checkbox[0].value is False
        # Verify URL parameters are initialized
        assert get_query_params(self.at)
        assert get_query_params(self.at)["check"] == ["False"]

    def test_checkbox_url_param_true(self):
        """Test checkbox with URL parameter set to True"""
        # Set initial URL parameter
        set_query_params(self.at, {"check": "True"})
        self.at.run()

        # Verify checkbox reflects URL state
        assert self.at.checkbox[0].value is True

    def test_checkbox_url_param_false(self):
        """Test checkbox with URL parameter set to False"""
        set_query_params(self.at, {"check": "False"})
        self.at.run()

        assert self.at.checkbox[0].value is False

    def test_checkbox_interaction_updates_url(self):
        """Test that checking/unchecking updates URL parameters"""
        self.at.run()

        # Initially unchecked and no URL params
        assert self.at.checkbox[0].value is False
        assert get_query_params(self.at)
        assert get_query_params(self.at)["check"] == ["False"]

        # Check the checkbox
        self.at.checkbox[0].check().run()

        # Verify URL parameter was updated
        assert get_query_params(self.at)["check"] == ["True"]
        assert self.at.checkbox[0].value is True

        # Uncheck the checkbox
        self.at.checkbox[0].uncheck().run()

        # Verify URL parameter was updated
        assert get_query_params(self.at)["check"] == ["False"]
        assert self.at.checkbox[0].value is False

    def test_checkbox_invalid_url_param(self):
        """Test checkbox behavior with invalid URL parameter value"""
        set_query_params(self.at, {"check": "invalid"})
        self.at.run()

        # Verify exception is raised
        assert self.at.exception

    def test_checkbox_empty_url_param(self):
        """Test checkbox behavior with empty URL parameter value"""
        set_query_params(self.at, {"check": ""})
        self.at.run()

        # Verify exception is raised
        assert self.at.exception

    def test_checkbox_multiple_url_values(self):
        """Test checkbox behavior with multiple URL parameter values"""
        # Set multiple values for the same parameter
        set_query_params(self.at, {"check": ["True", "False"]})
        self.at.run()

        # Should raise an exception
        assert self.at.exception

    def test_checkbox_with_default_true(self):
        """Test checkbox with default value set to True"""

        def app_with_default_true():
            import streamlit_permalink as st

            st.checkbox(
                "Default True Checkbox", value=True, url_key="check_default_true"
            )

        at = AppTest.from_function(app_with_default_true)
        at.run()

        # Verify checkbox is checked by default
        assert at.checkbox[0].value is True
        # Verify URL parameter is initialized to True
        assert get_query_params(at)["check_default_true"] == ["True"]

    def test_checkbox_case_insensitive_url_param(self):
        """Test checkbox with case-insensitive URL parameter values"""
        # Test with lowercase 'true'
        set_query_params(self.at, {"check": "true"})
        self.at.run()

        # Should accept lowercase 'true'
        assert not self.at.exception
        assert self.at.checkbox[0].value is True

        # Test with mixed case 'FaLsE'
        set_query_params(self.at, {"check": "FaLsE"})
        self.at.run()

        # Should accept mixed case 'FaLsE'
        assert not self.at.exception
        assert self.at.checkbox[0].value is False
        

def create_form_checkbox_app():
    import streamlit_permalink as stp
    import streamlit_permalink as st

    form = stp.form("test_form")
    with form:
        checkbox = form.checkbox("Form Checkbox", url_key="form_check")
        submitted = form.form_submit_button("Submit")


class TestFormCheckbox:
    def setup_method(self):
        self.at = AppTest.from_function(create_form_checkbox_app)

    def test_form_checkbox_default_state(self):
        """Test form checkbox with no URL parameters"""
        self.at.run()

        assert not self.at.exception

        # Verify checkbox exists and is unchecked by default
        assert len(self.at.checkbox) == 1
        assert self.at.checkbox[0].value is False
        # Verify URL parameters are initialized
        assert get_query_params(self.at)
        assert get_query_params(self.at)["form_check"] == ["False"]

    def test_form_checkbox_url_param_true(self):
        """Test form checkbox with URL parameter set to True"""
        set_query_params(self.at, {"form_check": "True"})
        self.at.run()

        assert self.at.checkbox[0].value is True

    def test_form_checkbox_url_param_false(self):
        """Test form checkbox with URL parameter set to False"""
        set_query_params(self.at, {"form_check": "False"})
        self.at.run()

        assert self.at.checkbox[0].value is False

    def test_form_checkbox_interaction_updates_url(self):
        """Test that checking/unchecking updates URL parameters after form submission"""
        self.at.run()

        # Initially unchecked and no URL params
        assert self.at.checkbox[0].value is False
        assert get_query_params(self.at)

        # Check the checkbox
        self.at.checkbox[0].check()
        # Submit the form
        self.at.button[0].click().run()

        # Verify URL parameter was updated after form submission
        assert get_query_params(self.at)["form_check"] == ["True"]
        assert self.at.checkbox[0].value is True

        # Uncheck the checkbox
        self.at.checkbox[0].uncheck()
        # Submit the form
        self.at.button[0].click().run()

        # Verify URL parameter was updated after form submission
        assert get_query_params(self.at)["form_check"] == ["False"]
        assert self.at.checkbox[0].value is False

    def test_form_checkbox_no_url_update_without_submit(self):
        """Test that URL parameters don't update until form is submitted"""
        self.at.run()

        # Initially unchecked and no URL params
        assert self.at.checkbox[0].value is False
        assert get_query_params(self.at)
        assert get_query_params(self.at)["form_check"] == ["False"]

        # Check the checkbox without submitting
        self.at.checkbox[0].check().run()

        # Verify URL parameters haven't changed
        assert get_query_params(self.at)
        assert get_query_params(self.at)["form_check"] == ["False"]
        # Now submit the form
        self.at.button[0].click().run()

        # Verify URL parameters updated after submission
        assert get_query_params(self.at)["form_check"] == ["True"]

    def test_form_checkbox_multiple_forms(self):
        """Test multiple checkboxes in different forms"""

        def multi_form_app():
            import streamlit_permalink as st

            form1 = st.form("form1")
            with form1:
                check1 = form1.checkbox("Checkbox 1", url_key="check1")
                form1.form_submit_button("Submit 1")

            form2 = st.form("form2")
            with form2:
                check2 = form2.checkbox("Checkbox 2", url_key="check2")
                form2.form_submit_button("Submit 2")

        at = AppTest.from_function(multi_form_app)
        at.run()

        # Test initial state
        assert len(at.checkbox) == 2
        assert all(not cb.value for cb in at.checkbox)

        # Test updating first form
        at.checkbox[0].check()
        at.button[0].click().run()
        assert get_query_params(at)["check1"] == ["True"]
        assert "check2" in get_query_params(at)

        # Test updating second form
        at.checkbox[1].check()
        at.button[1].click().run()
        assert get_query_params(at)["check1"] == ["True"]
        assert get_query_params(at)["check2"] == ["True"]
