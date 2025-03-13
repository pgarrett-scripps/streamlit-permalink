import datetime
import streamlit as st
import streamlit_permalink as stp

t = st.time_input("Set an alarm for", datetime.time(8, 45))
st.write("Alarm is set for", t)

stp.time_input("Set an alarm for", datetime.time(8, 45), key="time_input")

stp.time_input("Set an alarm for", datetime.time(8, 45, 30), key="time_input_sec")

# none
stp.time_input("Set an alarm for", None, key="time_input_none")


