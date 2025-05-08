from datetime import datetime
import pandas as pd
import streamlit as st


st.header("Imports", divider=True)
with st.echo("Imports"):
    from datetime import date, time
    import streamlit_permalink as stp
    import streamlit as st


st.header("Compression and Options", divider=True)
with st.echo("Consts"):

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


st.header("Forms", divider=True)
st.subheader('With stp.form("form")')
with st.echo("Form 1"):
    st.warning("Pressing enter to confirm text input counts as submitting the form")

    with stp.form("form"):
        is_checked_form1 = stp.checkbox(
            label="checkbox_form1", url_key="checkbox_form1"
        )
        st.caption(f"checkbox_form1: {is_checked_form1}")
        st.caption(f'query_params: {stp.get_query_params().get("checkbox_form1")}')

        text_input_form1 = stp.text_input(
            label="text_input_form1",
            value="xxx",
            max_chars=25,
            url_key="text_input_form1",
        )
        st.caption(f"text_input_form1: {text_input_form1}")
        st.caption(f'query_params: {stp.get_query_params().get("text_input_form1")}')

        stp.form_submit_button("Submit")


st.subheader('With stp.form("form2")')
with st.echo("Form 2"):
    form2 = stp.form("form2")
    is_checked_form2 = form2.checkbox(
        label="is_checked_form2", value=True, url_key="is_checked_form2"
    )
    form2.caption(f"is_checked_form2: {is_checked_form2}")
    form2.caption(f'query_params: {stp.get_query_params().get("is_checked_form2")}')

    number_input_form2 = form2.number_input(
        label="number_input_form2",
        min_value=1,
        max_value=100,
        value=42,
        url_key="number_input_form2",
    )

    form2.caption(f"number_input_form2: {number_input_form2}")
    form2.caption(f'query_params: {stp.get_query_params().get("number_input_form2")}')
    form2.form_submit_button("Submit")


st.header("Checkbox", divider=True)
with st.echo("Checkbox"):
    is_checked = stp.checkbox(label="checkbox", url_key="checkbox")
    st.caption(f"is_checked: {is_checked}")
    st.caption(f'query_params: {stp.get_query_params().get("checkbox")}')


# if toggle is available, use it
if hasattr(st, "toggle"):
    st.header("Toggle", divider=True)
    with st.echo("Toggle"):
        toggle = stp.toggle(label="toggle", url_key="toggle")
        st.caption(f"toggle: {toggle}")
        st.caption(f'query_params: {stp.get_query_params().get("toggle")}')


st.header("Radio", divider=True)
with st.echo("Radio"):
    radio = stp.radio(label="radio", options=OPTIONS, url_key="radio")
    st.caption(f"radio: {radio}")
    st.caption(f'query_params: {stp.get_query_params().get("radio")}')

st.header("Selectbox", divider=True)
with st.echo("Selectbox"):
    selectbox = stp.selectbox(label="selectbox", options=OPTIONS, url_key="selectbox")
    st.caption(f"selectbox: {selectbox}")
    st.caption(f'query_params: {stp.get_query_params().get("selectbox")}')

    # selectbox with accept_new_options if streamlit version is 1.45.0 or higher
    if st.__version__ >= "1.45.0":
        selectbox_accept_new = stp.selectbox(
            label="selectbox_accept_new",
            options=OPTIONS,
            accept_new_options=True,
            url_key="selectbox_accept_new",
        )
        st.caption(f"selectbox_accept_new: {selectbox_accept_new}")
        st.caption(f'query_params: {stp.get_query_params().get("selectbox_accept_new")}')

st.header("Multiselect", divider=True)
with st.echo("Multiselect"):
    multiselect = stp.multiselect(
        label="multiselect",
        options=OPTIONS,
        default=["Option A", 1],
        url_key="multiselect",
    )
    st.caption(f"multiselect: {multiselect}")
    st.caption(f'query_params: {stp.get_query_params().get("multiselect")}')

    # multiselect with accept_new_options if streamlit version is 1.45.0 or higher
    if st.__version__ >= "1.45.0":
        multiselect_accept_new = stp.multiselect(
            label="multiselect_accept_new",
            options=OPTIONS,
            default=["Option A", 1],
            accept_new_options=True,
            url_key="multiselect_accept_new",
        )
        st.caption(f"multiselect_accept_new: {multiselect_accept_new}")
        st.caption(f'query_params: {stp.get_query_params().get("multiselect_accept_new")}')

st.header("Number Sliders", divider=True)
with st.echo("Number Sliders"):
    # single and multi sliders with int values
    single_slider = stp.slider(
        label="single_slider",
        min_value=1,
        max_value=100,
        value=33,
        step=1,
        url_key="single_slider",
    )
    st.caption(f"single_slider: {single_slider}")
    st.caption(f'query_params: {stp.get_query_params().get("single_slider")}')

    multi_slider = stp.slider(
        label="multi_slider",
        min_value=1,
        max_value=100,
        value=[42, 67],
        step=1,
        url_key="multi_slider",
    )
    st.caption(f"multi_slider: {multi_slider}")
    st.caption(f'query_params: {stp.get_query_params().get("multi_slider")}')

st.header("Date Sliders", divider=True)
with st.echo("Date Sliders"):
    # single and multi sliders with dates as values
    single_date_slider = stp.slider(
        label="single_date_slider",
        min_value=date(2024, 1, 1),
        max_value=date(2024, 12, 31),
        value=date(2024, 1, 1),
        url_key="single_date_slider",
    )
    st.caption(f"single_date_slider: {single_date_slider}")
    st.caption(f'query_params: {stp.get_query_params().get("single_date_slider")}')

    multi_date_slider = stp.slider(
        label="multi_date_slider",
        min_value=date(2024, 1, 1),
        max_value=date(2024, 12, 31),
        value=[date(2024, 1, 1), date(2024, 12, 31)],
        url_key="multi_date_slider",
    )

    st.caption(f"multi_date_slider: {multi_date_slider}")
    st.caption(f'query_params: {stp.get_query_params().get("multi_date_slider")}')

st.header("Time Sliders", divider=True)
with st.echo("Time Sliders"):
    # single and multi time sliders
    single_time_slider = stp.slider(
        label="single_time_slider",
        min_value=time(0, 0, 0),
        max_value=time(23, 59, 59),
        value=time(12, 0, 0),
        url_key="single_time_slider",
    )
    st.caption(f"single_time_slider: {single_time_slider}")
    st.caption(f'query_params: {stp.get_query_params().get("single_time_slider")}')

    multi_time_slider = stp.slider(
        label="multi_time_slider",
        min_value=time(0, 0, 0),
        max_value=time(23, 59, 59),
        value=[time(12, 0, 0), time(13, 0, 0)],
        url_key="multi_time_slider",
    )
    st.caption(f"multi_time_slider: {multi_time_slider}")
    st.caption(f'query_params: {stp.get_query_params().get("multi_time_slider")}')


st.header("Select Sliders", divider=True)
with st.echo("Select Sliders"):
    # single and range select sliders
    select_slider = stp.select_slider(
        label="single_select_slider",
        options=OPTIONS,
        value=1,
        url_key="single_select_slider",
    )
    st.caption(f"select_slider: {select_slider}")
    st.caption(f'query_params: {stp.get_query_params().get("single_select_slider")}')

    range_select_slider = stp.select_slider(
        label="range_select_slider",
        options=OPTIONS,
        value=["Option A", 2],
        url_key="range_select_slider",
    )
    st.caption(f"range_select_slider: {range_select_slider}")
    st.caption(f'query_params: {stp.get_query_params().get("range_select_slider")}')


st.header("Text Input", divider=True)
with st.echo("Text Input"):
    text_input = stp.text_input(
        label="text_input", value="xxx", max_chars=25, url_key="text_input"
    )
    st.caption(f"text_input: {text_input}")
    st.caption(f'query_params: {stp.get_query_params().get("text_input")}')

st.header("Number Input", divider=True)
with st.echo("Number Input"):
    number_input = stp.number_input(
        label="number_input",
        min_value=1,
        max_value=100,
        value=42,
        step=1,
        url_key="number_input",
    )
    st.caption(f"number_input: {number_input}")
    st.caption(f'query_params: {stp.get_query_params().get("number_input")}')

st.header("Text Area", divider=True)
with st.echo("Text Area"):
    text_area = stp.text_area(label="text_area", url_key="text_area")
    st.caption(f"text_area: {text_area}")
    st.caption(f'query_params: {stp.get_query_params().get("text_area")}')

    text_area_compress = stp.text_area(
        label="text_area_compress", compress=True, url_key="text_area_compress"
    )
    st.caption(f"text_area_compress: {text_area_compress}")
    st.caption(f'query_params: {stp.get_query_params().get("text_area_compress")}')

    text_area_compress_custom = stp.text_area(
        label="text_area_compress_custom",
        compress=True,
        compressor=custom_compress,
        decompressor=custom_decompress,
        url_key="text_area_compress_custom",
    )
    st.caption(f"text_area_compress_custom: {text_area_compress_custom}")
    st.caption(f'query_params: {stp.get_query_params().get("text_area_compress_custom")}')

st.header("Date Input", divider=True)
with st.echo("Date Input"):
    # single and multi date inputs
    date_input = stp.date_input(label="date_input", url_key="date_input")
    st.caption(f"date_input: {date_input}")
    st.caption(f'query_params: {stp.get_query_params().get("date_input")}')

    multi_date_input = stp.date_input(
        label="multi_date_input",
        value=[date(2024, 1, 1), date(2024, 12, 31)],
        url_key="multi_date_input",
    )
    st.caption(f"multi_date_input: {multi_date_input}")
    st.caption(f'query_params: {stp.get_query_params().get("multi_date_input")}')

st.header("Time Input", divider=True)
with st.echo("Time Input"):
    # single and multi time inputs
    time_input = stp.time_input(label="time_input", url_key="time_input")
    st.caption(f"time_input: {time_input}")
    st.caption(f'query_params: {stp.get_query_params().get("time_input")}')

st.header("Color Picker", divider=True)
with st.echo("Color Picker"):
    color_picker = stp.color_picker(
        label="color_picker", value="#00EEFF", url_key="color_picker"
    )
    st.caption(f"color_picker: {color_picker}")
    st.caption(f'query_params: {stp.get_query_params().get("color_picker")}')

if hasattr(st, "pills"):
    st.header("Pills", divider=True)
    with st.echo("Pills"):
        pills_single = stp.pills(
            label="pills_single", options=OPTIONS, url_key="pills_single"
        )
        st.caption(f"pills_single: {pills_single}")
        st.caption(f'query_params: {stp.get_query_params().get("pills_single")}')

        pills_multi = stp.pills(
            label="pills_multi",
            options=OPTIONS,
            selection_mode="multi",
            url_key="pills_multi",
        )
        st.caption(f"pills_multi: {pills_multi}")
        st.caption(f'query_params: {stp.get_query_params().get("pills_multi")}')

# Add segmented control widgets if available
if hasattr(st, "segmented_control"):
    st.header("Segmented Control", divider=True)
    with st.echo("Segmented Control"):
        seg_single = stp.segmented_control(
            label="segmented_control_single",
            options=OPTIONS,
            url_key="segmented_control_single",
        )
        st.caption(f"seg_single: {seg_single}")
        st.caption(
            f'query_params: {stp.get_query_params().get("segmented_control_single")}'
        )

        seg_multi = stp.segmented_control(
            label="segmented_control_multi",
            options=OPTIONS,
            selection_mode="multi",
        )
        st.caption(f"seg_multi: {seg_multi}")
        st.caption(
            f'query_params: {stp.get_query_params().get("segmented_control_multi")}'
        )

# Add data editor widget if available
if hasattr(st, "data_editor"):
    st.header("Data Editor", divider=True)
    with st.echo("Data Editor"):
        example_df = pd.DataFrame(
            {
                "widgets": ["st.selectbox", "st.number_input", "st.text_area", "st.button"],
                "price": [20, 950, 250, 500],
                "favorite": [True, False, False, True],
                "category": [
                    "📊 Data Exploration",
                    "📈 Data Visualization",
                    "🤖 LLM",
                    "📊 Data Exploration",
                ],
                "appointment (datetime)": [
                    datetime(2024, 2, 5, 12, 30),
                    datetime(2023, 11, 10, 18, 0),
                    datetime(2024, 3, 11, 20, 10),
                    datetime(2023, 9, 12, 3, 0),
                ],
            }
        )
        df = stp.data_editor(
            example_df,
            url_key="example_data_editor1",
            num_rows="dynamic",
            compress=True,
            hide_index=True,
            column_config={
                "widgets": st.column_config.TextColumn(
                    "Widgets",
                    help="Streamlit **widget** commands 🎈",
                    default="st.",
                    max_chars=50,
                    validate=r"^st\.[a-z_]+$",
                ),
                "price": st.column_config.NumberColumn(
                    "Price (in USD)",
                    help="The price of the product in USD",
                    min_value=0,
                    max_value=1000,
                    step=1,
                    format="$%d",
                ),
                "favorite": st.column_config.CheckboxColumn(
                    "Your favorite?",
                    help="Select your **favorite** widgets",
                    default=False,
                ),
                "category": st.column_config.SelectboxColumn(
                    "App Category",
                    help="The category of the app",
                    width="medium",
                    options=[
                        "📊 Data Exploration",
                        "📈 Data Visualization",
                        "🤖 LLM",
                    ],
                    required=True,
                ),
                "appointment (datetime)": st.column_config.DatetimeColumn(
                    "Appointment (datetime)",
                    min_value=datetime(2023, 6, 1),
                    max_value=datetime(2025, 1, 1),
                    format="D MMM YYYY, h:mm a",
                    step=60,
                ),
            })


# if streamlit version is 1.45.0 or higher
if st.__version__ >= "1.45.0":
    st.header("Page Link", divider=True)
    with st.echo("Page Link"):
        st.info("Requires streamlit 1.45.0 or higher to parse the URL")
        st.caption("This page is linked to the following URL:")
        st.caption(stp.get_page_url())
