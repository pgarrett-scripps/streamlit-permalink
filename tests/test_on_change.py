from streamlit.testing.v1 import AppTest


def create_on_change_app():
    import streamlit_permalink as stp
    import streamlit as st

    # Initialize counter
    if "callback_count" not in st.session_state:
        st.session_state.callback_count = 0

    def on_change_callback():
        st.session_state.callback_count += 1

    # Checkbox with on_change
    stp.checkbox(
        "Checkbox with callback",
        key="callback",
        url_key="callback_param",
        on_change=on_change_callback,
    )

    # Display callback count
    st.write(f"Callback count: {st.session_state.callback_count}")


def test_on_change():
    """Test on_change callback works"""
    at = AppTest.from_function(create_on_change_app)
    at.run()

    # Initial state
    assert at.checkbox[0].value is False
    assert at.session_state.callback_count == 0

    # Check the checkbox to trigger on_change
    at.checkbox[0].check()
    at.run()

    # Verify callback was executed
    assert at.session_state.callback_count == 1

    # Verify URL was updated
    assert at.query_params["callback_param"] == ["True"]
