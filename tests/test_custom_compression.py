from streamlit.testing.v1 import AppTest
from .utils import get_query_params, set_query_params


def create_custom_compressed_app():
    import streamlit_permalink as stp

    # Custom compression functions
    def custom_compressor(text):
        return f"CUSTOM_{text}_COMPRESSED"

    def custom_decompressor(text):
        if text.startswith("CUSTOM_") and text.endswith("_COMPRESSED"):
            return text[7:-11]
        return text

    # Checkbox with custom compression
    stp.checkbox(
        "Custom Compressed",
        key="custom_compressed",
        url_key="custom_compressed",
        compress=True,
        compressor=custom_compressor,
        decompressor=custom_decompressor,
    )


def test_custom_compression():
    """Test checkbox with custom compression functions"""
    at = AppTest.from_function(create_custom_compressed_app)
    at.run()

    # Verify checkbox exists and is unchecked by default
    assert at.checkbox[0].value is False

    # Verify URL parameter is initialized with custom compressed value
    params = get_query_params(at)
    assert "custom_compressed" in params
    assert params["custom_compressed"][0] == "CUSTOM_False_COMPRESSED"

    # Check the checkbox
    at.checkbox[0].check()
    at.run()

    # Verify URL parameter was updated with custom compressed value
    params = get_query_params(at)
    assert params["custom_compressed"][0] == "CUSTOM_True_COMPRESSED"

    # Test decompression by setting URL parameter
    at2 = AppTest.from_function(create_custom_compressed_app)
    set_query_params(at2, {"custom_compressed": "CUSTOM_True_COMPRESSED"})
    at2.run()

    # Verify checkbox correctly decompressed the value
    assert at2.checkbox[0].value is True
