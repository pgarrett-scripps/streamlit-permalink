from streamlit.testing.v1 import AppTest
from .utils import get_query_params, set_query_params


def create_non_stateful_app():
    import streamlit_permalink as stp

    # Non-stateful checkbox
    stp.checkbox("Non-stateful Checkbox", key="non_stateful", stateful=False)


def test_non_stateful_checkbox():
    """Test non-stateful checkbox doesn't update URL"""
    at = AppTest.from_function(create_non_stateful_app)
    at.run()

    # Verify initial state
    assert at.checkbox[0].value is False

    # Check the checkbox
    at.checkbox[0].check()
    at.run()

    # Verify URL doesn't contain parameter for non-stateful checkbox
    params = get_query_params(at)
    assert "non_stateful" not in params

    # But the checkbox state should still change
    assert at.checkbox[0].value is True
