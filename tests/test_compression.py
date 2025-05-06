from streamlit.testing.v1 import AppTest
from .utils import get_query_params, set_query_params


def create_compressed_checkbox_app():
    import streamlit_permalink as stp

    # Simple checkbox with compression
    stp.checkbox(
        "Compressed Checkbox", key="compressed", url_key="compressed", compress=True
    )


def test_default_compression():
    """Test checkbox with default compression"""
    at = AppTest.from_function(create_compressed_checkbox_app)
    at.run()

    # Verify checkbox exists and is unchecked by default
    assert at.checkbox[0].value is False

    # Verify URL parameter is initialized with compressed value
    params = get_query_params(at)
    assert "compressed" in params
    # The compressed value should not be the raw "False" string
    assert params["compressed"][0] != "False"

    # Check the checkbox
    at.checkbox[0].check()
    at.run()

    # Verify URL parameter was updated with compressed value
    params = get_query_params(at)
    assert "compressed" in params
    # The compressed value should not be the raw "True" string
    assert params["compressed"][0] != "True"

    # Now set a compressed URL parameter and verify it's correctly decompressed
    compressed_true = params["compressed"][0]

    # Create a new app instance with this compressed value
    at2 = AppTest.from_function(create_compressed_checkbox_app)
    set_query_params(at2, {"compressed": compressed_true})
    at2.run()

    # Verify checkbox correctly decompressed the value
    assert at2.checkbox[0].value is True
