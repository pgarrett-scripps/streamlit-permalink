from datetime import time
import streamlit as st
import streamlit_permalink as stp

v = st.time_input("Time Input", key="time_input", step=60, value=time(12, 1, 10, 10))

st.caption(f"Time: {v}")
