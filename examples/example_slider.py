import streamlit as st
import streamlit_permalink as stp
from datetime import datetime, timedelta, date, time

from streamlit_permalink.exceptions import UrlParamError


st.slider("Default Slider", min_value=date(2020, 1, 1))
st.slider("Default Slider", value=[date(2020, 6, 15), date(2020, 12, 1)])

# Number Sliders
stp.slider("Step Slider", url_key="step_slider")
stp.slider("Multi Slider", min_value=0, max_value=10, value=[2, 4], step=2, url_key="multi_slider")

# Time Sliders
stp.slider("Time Slider", min_value=time(0, 0), max_value=time(23, 59), value=time(12, 0), step=timedelta(hours=1), key="time_slider")
stp.slider("Multi Time Slider", min_value=time(0, 0), max_value=time(23, 59), value=[time(12, 0), time(18, 0)], step=timedelta(hours=1), key="multi_time_slider")

# Date Sliders
stp.slider("Date Slider", min_value=date(2020, 1, 1), max_value=date(2020, 12, 31), value=date(2020, 6, 15), step=timedelta(days=1), key="date_slider")
stp.slider("Multi Date Slider", min_value=date(2020, 1, 1), max_value=date(2020, 12, 31), value=[date(2020, 6, 15), date(2020, 12, 1)], step=timedelta(days=14), key="multi_date_slider")


# date time slider
stp.slider("Date Time Slider", min_value=datetime(2020, 1, 1, 0, 0), max_value=datetime(2020, 12, 31, 23, 59), value=datetime(2020, 6, 15, 12, 0), step=timedelta(days=14, hours=1), key="date_time_slider")

# example slider without min/max (will throw error on reload)
try:
    st.caption(st.slider("Slider without min/max", value=-100, key="slider_without_min_max"))
except UrlParamError as e:
    st.error(e)

# will also throw error on reload
try:
    st.caption(st.slider("Slider Range", value=(-10,30), key="sliderrange"))
except UrlParamError as e:
    st.error(e)


# date slider with min/max but no value
try:
    st.caption(st.slider("Date Slider without value", min_value=date(2020, 1, 1), max_value=date(2020, 12, 31), key="date_slider_without_value"))
except UrlParamError as e:
    st.error(e)


