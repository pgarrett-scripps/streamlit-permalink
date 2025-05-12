from streamlit.testing.v1 import AppTest
import streamlit_permalink as st
import pytest
from .utils import get_query_params, set_query_params


def create_toggle_app():
    import streamlit_permalink as stp

    stp.toggle("Test Toggle", url_key="toggle")


def create_form_toggle_app():
    import streamlit_permalink as stp

    form = stp.form("test_form")
    with form:
        toggle = form.toggle("Form Toggle", url_key="form_toggle")
        submitted = form.form_submit_button("Submit")


@pytest.mark.skipif(
    not hasattr(st, "toggle"),
    reason="Toggle widget not available in this Streamlit version",
)
class TestToggle:
    def setup_method(self):
        self.at = AppTest.from_function(create_toggle_app)

    def test_toggle_default_state(self):
        """Test toggle with no URL parameters"""
        self.at.run()

        assert not self.at.exception

        # Verify toggle exists and is unchecked by default
        assert len(self.at.toggle) == 1
        assert self.at.toggle[0].value is False
        # Verify URL parameters are initialized
        assert get_query_params(self.at)
        assert get_query_params(self.at)["toggle"] == ["False"]

    def test_toggle_url_param_true(self):
        """Test toggle with URL parameter set to True"""
        # Set initial URL parameter
        set_query_params(self.at, {"toggle": "True"})
        self.at.run()

        # Verify toggle reflects URL state
        assert self.at.toggle[0].value is True

    def test_toggle_url_param_false(self):
        """Test toggle with URL parameter set to False"""
        set_query_params(self.at, {"toggle": "False"})
        self.at.run()

        assert self.at.toggle[0].value is False

    def test_toggle_interaction_updates_url(self):
        """Test that toggling on/off updates URL parameters"""
        self.at.run()

        # Initially off and no URL params
        assert self.at.toggle[0].value is False
        assert get_query_params(self.at)
        assert get_query_params(self.at)["toggle"] == ["False"]
        # Turn toggle on
        self.at.toggle[0].set_value(True).run()

        # Verify URL parameter was updated
        assert get_query_params(self.at)["toggle"] == ["True"]
        assert self.at.toggle[0].value is True

        # Turn toggle off
        self.at.toggle[0].set_value(False).run()

        # Verify URL parameter was updated
        assert get_query_params(self.at)["toggle"] == ["False"]
        assert self.at.toggle[0].value is False

    def test_toggle_invalid_url_param(self):
        """Test toggle behavior with invalid URL parameter value"""
        set_query_params(self.at, {"toggle": "invalid"})
        self.at.run()

        # Verify exception is raised
        assert self.at.exception

    def test_toggle_empty_url_param(self):
        """Test toggle behavior with empty URL parameter value"""
        set_query_params(self.at, {"toggle": ""})
        self.at.run()

        # Verify exception is raised
        assert self.at.exception

    def test_toggle_multiple_url_values(self):
        """Test toggle behavior with multiple URL parameter values"""
        # Set multiple values for the same parameter
        set_query_params(self.at, {"toggle": ["True", "False"]})
        self.at.run()

        # Should raise an exception
        assert self.at.exception

    def test_toggle_with_default_true(self):
        """Test toggle with default value set to True"""

        def app_with_default_true():
            import streamlit as st
            import streamlit_permalink as st

            st.toggle("Default True Toggle", value=True, url_key="toggle_default_true")

        at = AppTest.from_function(app_with_default_true)
        at.run()

        # Verify toggle is on by default
        assert at.toggle[0].value is True
        # Verify URL parameter is initialized to True
        assert get_query_params(at)["toggle_default_true"] == ["True"]

    def test_toggle_case_insensitive_url_param(self):
        """Test toggle with case-insensitive URL parameter values"""
        # Test with lowercase 'true'
        set_query_params(self.at, {"toggle": "true"})
        self.at.run()

        # Should accept lowercase 'true'
        assert not self.at.exception
        assert self.at.toggle[0].value is True

        # Test with mixed case 'FaLsE'
        set_query_params(self.at, {"toggle": "FaLsE"})
        self.at.run()

        # Should accept mixed case 'FaLsE'
        assert not self.at.exception
        assert self.at.toggle[0].value is False


@pytest.mark.skipif(
    not hasattr(st, "toggle"),
    reason="Toggle widget not available in this Streamlit version",
)
class TestFormToggle:
    def setup_method(self):
        self.at = AppTest.from_function(create_form_toggle_app)

    def test_form_toggle_default_state(self):
        """Test form toggle with no URL parameters"""
        self.at.run()

        assert not self.at.exception

        # Verify toggle exists and is unchecked by default
        assert len(self.at.toggle) == 1
        assert self.at.toggle[0].value is False
        # Verify URL parameters are initialized
        assert get_query_params(self.at)
        assert get_query_params(self.at)["form_toggle"] == ["False"]

    def test_form_toggle_url_param_true(self):
        """Test form toggle with URL parameter set to True"""
        set_query_params(self.at, {"form_toggle": "True"})
        self.at.run()

        assert get_query_params(self.at)
        assert get_query_params(self.at)["form_toggle"] == ["True"]

        assert self.at.toggle[0].value is True

    def test_form_toggle_url_param_false(self):
        """Test form toggle with URL parameter set to False"""
        set_query_params(self.at, {"form_toggle": "False"})
        self.at.run()

        assert get_query_params(self.at)
        assert get_query_params(self.at)["form_toggle"] == ["False"]

        assert self.at.toggle[0].value is False

    def test_form_toggle_interaction_updates_url(self):
        """Test that toggling updates URL parameters after form submission"""
        self.at.run()

        # Initially off and no URL params
        assert self.at.toggle[0].value is False
        assert get_query_params(self.at)
        assert get_query_params(self.at)["form_toggle"] == ["False"]
        # Turn toggle on
        self.at.toggle[0].set_value(True)
        # Submit the form
        self.at.button[0].click().run()

        # Verify URL parameter was updated after form submission
        assert get_query_params(self.at)["form_toggle"] == ["True"]
        assert self.at.toggle[0].value is True

        # Turn toggle off
        self.at.toggle[0].set_value(False)
        # Submit the form
        self.at.button[0].click().run()

        # Verify URL parameter was updated after form submission
        assert get_query_params(self.at)["form_toggle"] == ["False"]
        assert self.at.toggle[0].value is False

    def test_form_toggle_no_url_update_without_submit(self):
        """Test that URL parameters don't update until form is submitted"""
        self.at.run()

        # Initially off and no URL params
        assert self.at.toggle[0].value is False
        assert get_query_params(self.at)
        assert get_query_params(self.at)["form_toggle"] == ["False"]

        # Turn toggle on without submitting
        self.at.toggle[0].set_value(True).run()

        # Verify URL parameters haven't changed
        assert get_query_params(self.at)
        assert get_query_params(self.at)["form_toggle"] == ["False"]

        # Now submit the form
        self.at.button[0].click().run()

        # Verify URL parameters updated after submission
        assert get_query_params(self.at)["form_toggle"] == ["True"]

    def test_form_toggle_multiple_forms(self):
        """Test multiple toggles in different forms"""

        def multi_form_app():
            import streamlit as st
            import streamlit_permalink as st

            form1 = st.form("form1")
            with form1:
                toggle1 = form1.toggle("Toggle 1", url_key="toggle1")
                form1.form_submit_button("Submit 1")

            form2 = st.form("form2")
            with form2:
                toggle2 = form2.toggle("Toggle 2", url_key="toggle2")
                form2.form_submit_button("Submit 2")

        at = AppTest.from_function(multi_form_app)
        at.run()

        # Test initial state
        assert len(at.toggle) == 2
        assert all(not t.value for t in at.toggle)

        # Test updating first form
        at.toggle[0].set_value(True)
        at.button[0].click().run()
        assert get_query_params(at)["toggle1"] == ["True"]
        assert "toggle2" in get_query_params(at)

        # Test updating second form
        at.toggle[1].set_value(True)
        at.button[1].click().run()
        assert get_query_params(at)["toggle1"] == ["True"]
        assert get_query_params(at)["toggle2"] == ["True"]
