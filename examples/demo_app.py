import streamlit as st
import streamlit_permalink as stp

st.caption("form checkbox (url_key='checkbox')")
with stp.form("form"):
    is_checked = stp.checkbox("checkbox", url_key="checkbox")
    stp.form_submit_button("Submit")

st.caption("radio (url_key='radio')")
radio = stp.radio("radio", options=['Hello', 'World'], index=1, url_key="radio")

st.caption("text_input with compression (url_key='text_input')")
text_input = stp.text_input("text_input (compressed)", value="Hello World", url_key="text_input", compress=True)

page_link = stp.get_page_url()

st.caption("Page Link")
st.write(page_link)