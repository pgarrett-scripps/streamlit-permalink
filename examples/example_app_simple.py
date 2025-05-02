from datetime import date, time

import streamlit_permalink as stp
import streamlit as st

import gzip
import base64


def custom_compress(value: str) -> str:
    # Compress the string and encode the binary result as base64
    compressed = gzip.compress(value.encode("utf-8"))
    return base64.b64encode(compressed).decode("utf-8")


def custom_decompress(value: str) -> str:
    # Decode the base64 string back to binary and then decompress
    binary_data = base64.b64decode(value.encode("utf-8"))
    return gzip.decompress(binary_data).decode("utf-8")


OPTIONS = ["Option A", "Option B", 1, 2, {"Hello": "World"}]

with stp.form("form"):
    is_checked = stp.checkbox("checkbox", url_key="checkbox")
    stp.form_submit_button("Submit")

form2 = stp.form("form2")
is_checked_default = form2.checkbox(
    "checkbox default", value=True, url_key="checkbox_default"
)
form2.form_submit_button("Submit")

radio = stp.radio("radio", options=OPTIONS, url_key="radio")

selectbox = stp.selectbox("selectbox", options=OPTIONS, url_key="selectbox")
multiselect = stp.multiselect(
    "multiselect", options=OPTIONS, default=["Option A", 1], url_key="multiselect"
)

# single and multi sliders with int values
single_slider = stp.slider(
    "single_slider", min_value=1, max_value=100, value=33, url_key="single_slider"
)
multi_slider = stp.slider(
    "multi_slider", min_value=1, max_value=100, value=[42, 67], url_key="multi_slider"
)

# single and multi sliders with dates as values
single_date_slider = stp.slider(
    "single_date_slider",
    min_value=date(2024, 1, 1),
    max_value=date(2024, 12, 31),
    value=date(2024, 1, 1),
    url_key="single_date_slider",
)
multi_date_slider = stp.slider(
    "multi_date_slider",
    min_value=date(2024, 1, 1),
    max_value=date(2024, 12, 31),
    value=[date(2024, 1, 1), date(2024, 12, 31)],
    url_key="multi_date_slider",
)

# single and multi time sliders
single_time_slider = stp.slider(
    "single_time_slider",
    min_value=time(0, 0, 0),
    max_value=time(23, 59, 59),
    value=time(12, 0, 0),
    url_key="single_time_slider",
)
multi_time_slider = stp.slider(
    "multi_time_slider",
    min_value=time(0, 0, 0),
    max_value=time(23, 59, 59),
    value=[time(12, 0, 0), time(13, 0, 0)],
    url_key="multi_time_slider",
)

# single and range select sliders
select_slider = stp.select_slider(
    "single_select_slider", options=OPTIONS, value=1, url_key="single_select_slider"
)
range_select_slider = stp.select_slider(
    "range_select_slider",
    options=OPTIONS,
    value=["Option A", 2],
    url_key="range_select_slider",
)

text_input = stp.text_input(
    "text_input", value="xxx", url_key="text_input", max_chars=25
)
number_input = stp.number_input(
    "number_input", min_value=1, max_value=100, value=42, url_key="number_input"
)


text_area = stp.text_area("text_area", url_key="text_area")
text_area_compress = stp.text_area(
    "text_area_compress", url_key="text_area_compress", compress=True
)
text_area_compress_custom = stp.text_area(
    "text_area_compress_custom",
    url_key="text_area_compress_custom",
    compress=True,
    compressor=custom_compress,
    decompressor=custom_decompress,
)

# single and multi date inputs
date_input = stp.date_input("date_input", url_key="date_input")
multi_date_input = stp.date_input(
    "multi_date_input",
    value=[date(2024, 1, 1), date(2024, 12, 31)],
    url_key="multi_date_input",
)

# single and multi time inputs
time_input = stp.time_input("time_input", url_key="time_input")

color_picker = stp.color_picker("color_picker", value="#00EEFF", url_key="color_picker")

if hasattr(st, "pills"):
    pills_single = stp.pills("pills_single", OPTIONS, url_key="pills_single")
    pills_multi = stp.pills(
        "pills_multi", OPTIONS, selection_mode="multi", url_key="pills_multi"
    )

# Add segmented control widgets if available
if hasattr(st, "segmented_control"):
    seg_single = stp.segmented_control(
        "segmented_control_single", OPTIONS, url_key="segmented_control_single"
    )
    seg_multi = stp.segmented_control(
        "segmented_control_multi",
        OPTIONS,
        selection_mode="multi",
        url_key="segmented_control_multi",
    )

# if toggle is available, use it
if hasattr(st, "toggle"):
    toggle = stp.toggle("toggle", url_key="toggle")


st.caption("Page URL and query parameters:")
st.code(stp.get_page_url())
st.code(stp.get_query_params())


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
    "custom_compress",
    "custom_decompress",
    "base64",
    "gzip",
]
for i in irrelevant:
    if i in loc:
        del loc[i]
st.write(loc)


# if text == error, rerun the app
if text_input == "error":
    st.error("error")
    st.stop()
