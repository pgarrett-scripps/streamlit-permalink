import streamlit as st
import streamlit_permalink as stp
if 'count' not in st.session_state:
    st.session_state.count = 0

def increment_counter():
    st.session_state.count += 1

stp.checkbox('Increment', on_change=increment_counter, url_key='increment')

st.write(st.session_state.count)
