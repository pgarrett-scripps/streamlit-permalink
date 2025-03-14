import streamlit as st
from datetime import date, time

import streamlit_permalink as st

OPTIONS = ['Option A', 'Option B', 1, 2, {"Hello": "World"}]

with st.form('form'):
    is_checked = st.checkbox('checkbox', url_key='checkbox')
    is_checked_default = st.checkbox('checkbox default', value=True, url_key='checkbox_default')


    radio = st.radio('radio', options=OPTIONS, url_key='radio')
    selectbox = st.selectbox('selectbox', options=OPTIONS, url_key='selectbox')
    multiselect = st.multiselect('multiselect', options=OPTIONS, default=['Option A', 1], url_key='multiselect')

    # single and multi sliders with int values
    single_slider = st.slider('single_slider', min_value=1, max_value=100, value=33, url_key='single_slider')
    multi_slider = st.slider('multi_slider', min_value=1, max_value=100, value=[42, 67], url_key='multi_slider')

    # single and multi sliders with dates as values
    single_date_slider = st.slider('single_date_slider', min_value=date(2024, 1, 1), max_value=date(2024, 12, 31), value=date(2024, 1, 1), url_key='single_date_slider')
    multi_date_slider = st.slider('multi_date_slider', min_value=date(2024, 1, 1), max_value=date(2024, 12, 31), value=[date(2024, 1, 1), date(2024, 12, 31)], url_key='multi_date_slider')

    # single and multi time sliders
    single_time_slider = st.slider('single_time_slider', min_value=time(0, 0, 0), max_value=time(23, 59, 59), value=time(12, 0, 0), url_key='single_time_slider')
    multi_time_slider = st.slider('multi_time_slider', min_value=time(0, 0, 0), max_value=time(23, 59, 59), value=[time(12, 0, 0), time(13, 0, 0)], url_key='multi_time_slider')

    # single and range select sliders
    select_slider = st.select_slider('single_select_slider', options=OPTIONS, value=1, url_key='single_select_slider')
    range_select_slider = st.select_slider('range_select_slider', options=OPTIONS, value=["Option A", 2], url_key='range_select_slider')

    text_input = st.text_input('text_input', value='xxx', url_key='text_input', max_chars=25)
    number_input = st.number_input('number_input', min_value=1, max_value=100, value=42, url_key='number_input')
    text_area = st.text_area('text_area', url_key='text_area')

    # single and multi date inputs
    date_input = st.date_input('date_input', url_key='date_input')
    multi_date_input = st.date_input('multi_date_input', value=[date(2024, 1, 1), date(2024, 12, 31)], url_key='multi_date_input')

    # single and multi time inputs
    time_input = st.time_input('time_input', url_key='time_input')

    color_picker = st.color_picker('color_picker', value='#00EEFF', url_key='color_picker')

    if hasattr(st, 'pills'):
        pills_single = st.pills('pills_single', ['Option A', 'Option B', 'Option C'], url_key='pills_single')
        pills_multi = st.pills('pills_multi', ['Option A', 'Option B', 'Option C'], selection_mode='multi', url_key='pills_multi')

    # Add segmented control widgets if available
    if hasattr(st, 'segmented_control'):
        seg_single = st.segmented_control(
            "segmented_control_single", 
            ["Option A", "Option B", "Option C"], 
            url_key='segmented_control_single'
        )
        seg_multi = st.segmented_control(
            "segmented_control_multi", 
            ["Option A", "Option B", "Option C"],
            selection_mode="multi",
            url_key='segmented_control_multi'
        )

    # if toggle is available, use it
    if hasattr(st, 'toggle'):
        toggle = st.toggle('toggle', url_key='toggle')
        
    st.form_submit_button('Submit')

loc = locals().copy()
irrelevant = [
    "__name__",
    "__doc__",
    "__package__",
    "__loader__",
    "__spec__",
    "__file__",
    "__builtins__",
    "st",
    "__streamlitmagic__",
    "stp",
    "datetime",
    "date",
    "time",
]
for i in irrelevant:
    if i in loc:
        del loc[i]
st.write(loc)
