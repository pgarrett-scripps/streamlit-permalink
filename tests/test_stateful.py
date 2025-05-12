from streamlit.testing.v1 import AppTest

from .utils import get_query_params, set_query_params


def create_stateful_app():
    import streamlit_permalink as stp

    # Stateful checkbox (default)
    stp.checkbox("Stateful Checkbox", key="stateful", url_key="stateful_param")


def test_stateful_checkbox():
    """Test stateful checkbox updates URL"""
    at = AppTest.from_function(create_stateful_app)
    at.run()

    # Verify initial state
    assert at.checkbox[0].value is False
    assert "stateful_param" in get_query_params(at)

    # Check the checkbox
    at.checkbox[0].check()
    at.run()

    # Verify URL was updated
    assert get_query_params(at)["stateful_param"] == ["True"]
