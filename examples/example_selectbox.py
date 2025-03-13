import streamlit as st
import streamlit_permalink as stp

stp.selectbox("Select a fruit", options=["Apple", "Banana", "Cherry"], url_key="fruit")

# test format
def format_func(x):
    return f"Formatted {x}"
stp.selectbox("Select a fruit", options=["Apple", "Banana", "Cherry"], url_key="format", format_func=format_func)

# test form
form = stp.form("form")

