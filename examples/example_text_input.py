import streamlit as st
import streamlit_permalink as stp

stp.text_input("Basic Text Input", value="", url_key="text")
stp.text_input("Limited Text Input", max_chars=10, url_key="limited_text")
stp.text_input("Default Value Text", value="default", url_key="default_text")

with stp.form("test_form"):
    text = stp.text_input("Form Text Input", url_key="form_text")
    limited = stp.text_input("Form Limited Text", max_chars=10, url_key="form_limited")
    submitted = stp.form_submit_button("Submit")




