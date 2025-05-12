from streamlit.testing.v1 import AppTest


from streamlit_permalink import NONE_URL_VALUE, EMPTY_LIST_URL_VALUE
from .utils import get_query_params, set_query_params


def create_multiselect_app():
    import streamlit_permalink as stp

    OPTIONS = ["Option A", "Option B", "Option C"]
    stp.multiselect("Test Multiselect", options=OPTIONS, url_key="multi")


def create_form_multiselect_app():
    import streamlit_permalink as stp

    form = stp.form("test_form")
    with form:
        OPTIONS = ["Option A", "Option B", "Option C"]
        multiselect = form.multiselect(
            "Form Multiselect", options=OPTIONS, url_key="form_multi"
        )
        submitted = form.form_submit_button("Submit")


def create_multiselect_with_default_app():
    import streamlit_permalink as stp

    OPTIONS = ["Option A", "Option B", "Option C"]
    stp.multiselect(
        "Default Multiselect",
        options=OPTIONS,
        default=["Option B"],
        url_key="default_multi",
    )


def create_multiselect_with_nonstring_app():
    import streamlit_permalink as stp

    # Non-string options
    OPTIONS = [1, 2, 3, "Hello", "World"]
    stp.multiselect("Number Multiselect", options=OPTIONS, url_key="num_multi")


def create_multiselect_with_specialchars_app():
    import streamlit_permalink as stp

    # Options with special characters
    OPTIONS = ["Option with spaces", "Option/with/slashes", "Option?with&symbols"]
    stp.multiselect(
        "Special Chars Multiselect", options=OPTIONS, url_key="special_multi"
    )


def create_multiselect_with_duplicate_string_options_app():
    import streamlit_permalink as stp

    # Options that are not unique when cast to strings
    OPTIONS = [1, "1", 2, True, "True"]
    stp.multiselect(
        "Duplicate String Options", options=OPTIONS, url_key="duplicate_multi"
    )


def create_empty_options_app():
    import streamlit_permalink as stp

    EMPTY_OPTIONS = []
    stp.multiselect("Empty Options", options=EMPTY_OPTIONS, url_key="empty_multi")


class TestMultiselect:
    def setup_method(self):
        self.at = AppTest.from_function(create_multiselect_app)
        self.OPTIONS = ["Option A", "Option B", "Option C"]

    def test_multiselect_default_state(self):
        """Test multiselect with no URL parameters"""
        self.at.run()

        assert not self.at.exception
        assert len(self.at.multiselect) == 1
        assert self.at.multiselect[0].value == []
        assert get_query_params(self.at)["multi"] == [EMPTY_LIST_URL_VALUE]

    def test_multiselect_url_param(self):
        """Test multiselect with URL parameters set"""
        set_query_params(self.at, {"multi": ["Option A", "Option C"]})
        self.at.run()

        assert self.at.multiselect[0].value == ["Option A", "Option C"]

    def test_multiselect_interaction_updates_url(self):
        """Test that selecting/deselecting updates URL parameters"""
        self.at.run()

        # Test initial state
        assert get_query_params(self.at)["multi"] == [EMPTY_LIST_URL_VALUE]
        assert self.at.multiselect[0].value == []
        assert self.at.multiselect[0].indices == []

        # Test set_value method
        self.at.multiselect[0].set_value(["Option A", "Option B"]).run()
        assert get_query_params(self.at)["multi"] == ["Option A", "Option B"]
        assert self.at.multiselect[0].indices == [0, 1]

        # Test select method
        self.at.multiselect[0].select("Option C").run()
        assert get_query_params(self.at)["multi"] == [
            "Option A",
            "Option B",
            "Option C",
        ]

        # Test unselect method
        self.at.multiselect[0].unselect("Option B").run()
        assert get_query_params(self.at)["multi"] == ["Option A", "Option C"]

        # Test clearing all selections
        self.at.multiselect[0].set_value([]).run()
        assert get_query_params(self.at)["multi"] == [EMPTY_LIST_URL_VALUE]

    def test_multiselect_invalid_url_param(self):
        """Test multiselect behavior with invalid URL parameter value"""
        set_query_params(self.at, {"multi": ["Invalid Option"]})
        self.at.run()
        assert self.at.exception


class TestFormMultiselect:
    def setup_method(self):
        self.at = AppTest.from_function(create_form_multiselect_app)
        self.OPTIONS = ["Option A", "Option B", "Option C"]

    def test_form_multiselect_default_state(self):
        """Test form multiselect with no URL parameters"""
        self.at.run()

        assert not self.at.exception
        assert len(self.at.multiselect) == 1
        assert self.at.multiselect[0].value == []
        assert get_query_params(self.at)["form_multi"] == [EMPTY_LIST_URL_VALUE]

    def test_form_multiselect_url_param(self):
        """Test form multiselect with URL parameters set"""
        set_query_params(self.at, {"form_multi": ["Option A", "Option C"]})
        self.at.run()

        assert self.at.multiselect[0].value == ["Option A", "Option C"]

    def test_form_multiselect_interaction_updates_url(self):
        """Test that selections update URL parameters after form submission"""
        self.at.run()

        # Test set_value and submit
        self.at.multiselect[0].set_value(["Option A", "Option B"])
        self.at.button[0].click().run()
        assert get_query_params(self.at)["form_multi"] == ["Option A", "Option B"]
        assert self.at.multiselect[0].indices == [0, 1]

        # Test select and submit
        self.at.multiselect[0].select("Option C")
        self.at.button[0].click().run()
        assert get_query_params(self.at)["form_multi"] == [
            "Option A",
            "Option B",
            "Option C",
        ]

        # Test unselect and submit
        self.at.multiselect[0].unselect("Option B")
        self.at.button[0].click().run()
        assert get_query_params(self.at)["form_multi"] == ["Option A", "Option C"]


class TestMultiselectAdditional:
    def test_multiselect_with_default_values(self):
        """Test multiselect initialized with default values"""
        at = AppTest.from_function(create_multiselect_with_default_app)
        at.run()

        assert not at.exception
        assert at.multiselect[0].value == ["Option B"]
        assert get_query_params(at)["default_multi"] == ["Option B"]

        # Clear the selection
        at.multiselect[0].set_value([]).run()
        assert at.multiselect[0].value == []
        assert get_query_params(at)["default_multi"] == [EMPTY_LIST_URL_VALUE]

    def test_multiselect_empty_options_error(self):
        """Test error when multiselect options list is empty"""
        # Define an app with empty options

        at = AppTest.from_function(create_empty_options_app)
        at.run()

        # Should raise an exception due to empty options list
        assert at.exception
        # The error should contain relevant information
        # (not checking specific error message as it may vary)

    def test_multiselect_with_nonstring_options(self):
        """Test multiselect with non-string options (numbers, booleans)"""
        at = AppTest.from_function(create_multiselect_with_nonstring_app)
        at.run()

        assert not at.exception
        # Test setting values with non-string types
        at.multiselect[0].set_value(["1", "Hello"]).run()

        # Values are preserved as original types in the widget
        assert len(at.multiselect[0].value) == 2
        assert 1 in at.multiselect[0].value
        assert "Hello" in at.multiselect[0].value

        # URL params should have string representations
        assert get_query_params(at)["num_multi"] == ["1", "Hello"]

        # Test setting from URL with string representations
        set_query_params(at, {"num_multi": ["2", "World"]})
        at.run()
        assert not at.exception
        assert len(at.multiselect[0].value) == 2
        assert 2 in at.multiselect[0].value
        assert "World" in at.multiselect[0].value

    def test_multiselect_with_special_chars(self):
        """Test multiselect with options containing spaces and special characters"""
        at = AppTest.from_function(create_multiselect_with_specialchars_app)
        at.run()

        assert not at.exception

        # Select all options
        at.multiselect[0].set_value(
            ["Option with spaces", "Option/with/slashes", "Option?with&symbols"]
        ).run()

        # Check URL parameters are properly handled
        params = get_query_params(at)
        assert "Option with spaces" in params["special_multi"]
        assert "Option/with/slashes" in params["special_multi"]
        assert "Option?with&symbols" in params["special_multi"]

        # Test setting just one option from URL
        set_query_params(at, {"special_multi": ["Option?with&symbols"]})
        at.run()
        assert not at.exception
        assert at.multiselect[0].value == ["Option?with&symbols"]

    def test_multiselect_select_all_and_unselect_all(self):
        """Test selecting and unselecting all options"""
        at = AppTest.from_function(create_multiselect_app)
        at.run()

        # Select all options one by one
        for option in ["Option A", "Option B", "Option C"]:
            at.multiselect[0].select(option).run()

        # Check all are selected
        assert sorted(at.multiselect[0].value) == sorted(
            ["Option A", "Option B", "Option C"]
        )
        assert sorted(get_query_params(at)["multi"]) == sorted(
            ["Option A", "Option B", "Option C"]
        )

        # Unselect all options one by one
        for option in ["Option A", "Option B", "Option C"]:
            at.multiselect[0].unselect(option).run()

        # Check all are unselected
        assert at.multiselect[0].value == []
        assert get_query_params(at)["multi"] == [EMPTY_LIST_URL_VALUE]

        # Test setting all at once
        at.multiselect[0].set_value(["Option A", "Option B", "Option C"]).run()
        assert sorted(at.multiselect[0].value) == sorted(
            ["Option A", "Option B", "Option C"]
        )

        # Test clearing all at once
        at.multiselect[0].set_value([]).run()
        assert at.multiselect[0].value == []

    def test_multiselect_duplicate_string_options_error(self):
        """Test error when multiselect options are not unique when cast to strings"""
        at = AppTest.from_function(create_multiselect_with_duplicate_string_options_app)
        at.run()

        # Should raise an exception due to duplicate string representations
        assert at.exception
