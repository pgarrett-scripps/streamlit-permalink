import streamlit as st
import streamlit_permalink as stp

stp.toggle("Toggle", url_key="toggle")
stp.toggle("Toggle", key="toggle_key")
stp.toggle("Default Toggle", value=True, url_key="toggle_default")

stp.toggle(label="label parms", value=False, key='label_params', help=None, on_change=None, args=None, kwargs=None, disabled=False, label_visibility="visible")

# test sesion state
if 'toggle_count' not in st.session_state:
    st.session_state['toggle_count'] = 0

def on_change():   
    st.session_state['toggle_count'] += 1

stp.toggle("Toggle with on_change", url_key="toggle_on_change", on_change=on_change)

st.write(f"Toggle count: {st.session_state['toggle_count']}")

with stp.form("form"):
    stp.toggle("Form Toggle", url_key="form_toggle")
    stp.form_submit_button("Submit")


