from datetime import date, datetime, time

import streamlit_permalink as stp
import streamlit as st

import pandas as pd

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
        "birthday": [
            date(1980, 1, 1),
            date(1990, 5, 3),
            date(1974, 5, 19),
            date(2001, 8, 17),
        ],
        "appointment (time)": [
            time(12, 30),
            time(18, 0),
            time(9, 10),
            time(16, 25),
        ],
        "json": [
            {"foo": "bar", "bar": "baz"},
            {"foo": "baz", "bar": "qux"},
            {"foo": "qux", "bar": "foo"},
            None,
        ],
        "sales": [
            [0, 4, 26, 80, 100, 40],
            [80, 20, 80, 35, 40, 100],
            [10, 20, 80, 80, 70, 0],
            [10, 100, 20, 100, 30, 100],
        ],
        "links": [
            "https://roadmap.streamlit.app",
            "https://extras.streamlit.app",
            "https://issues.streamlit.app",
            "https://30days.streamlit.app",
        ],
        "images": [
            "https://storage.googleapis.com/s4a-prod-share-preview/default/st_app_screenshot_image/5435b8cb-6c6c-490b-9608-799b543655d3/Home_Page.png",
            "https://storage.googleapis.com/s4a-prod-share-preview/default/st_app_screenshot_image/ef9a7627-13f2-47e5-8f65-3f69bb38a5c2/Home_Page.png",
            "https://storage.googleapis.com/s4a-prod-share-preview/default/st_app_screenshot_image/31b99099-8eae-4ff8-aa89-042895ed3843/Home_Page.png",
            "https://storage.googleapis.com/s4a-prod-share-preview/default/st_app_screenshot_image/6a399b09-241e-4ae7-a31f-7640dc1d181e/Home_Page.png",
        ],
        "sales (area)": [
            [0, 4, 26, 80, 100, 40],
            [80, 20, 80, 35, 40, 100],
            [10, 20, 80, 80, 70, 0],
            [10, 100, 20, 100, 30, 100],
        ],
    }
)

df = stp.data_editor(
    example_df,
    url_key="example_data_editor1",
    num_rows="dynamic",
    compress=True,
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
        "birthday": st.column_config.DateColumn(
            "Birthday",
            min_value=date(1900, 1, 1),
            max_value=date(2005, 1, 1),
            format="DD.MM.YYYY",
            step=1,
        ),
        "appointment (time)": st.column_config.TimeColumn(
            "Appointment (time)",
            min_value=time(8, 0, 0),
            max_value=time(19, 0, 0),
            format="hh:mm a",
            step=60,
        ),
        "json": st.column_config.JsonColumn(
            "JSON Data",
            help="JSON strings or objects",
            width="large",
        ),
        "sales": st.column_config.ListColumn(
            "Sales (last 6 months)",
            help="The sales volume in the last 6 months",
            width="medium",
        ),
        "links": st.column_config.LinkColumn(
            "Trending apps",
            help="The top trending Streamlit apps",
            validate=r"^https://[a-z]+\.streamlit\.app$",
            max_chars=100,
            display_text=r"https://(.*?)\.streamlit\.app",
        ),
        "images": st.column_config.ImageColumn(
            "Preview Image", help="Streamlit app preview screenshots"
        ),
        "sales (area)": st.column_config.AreaChartColumn(
            "Sales (last 6 months)",
            width="medium",
            help="The sales volume in the last 6 months",
            y_min=0,
            y_max=100,
        ),
    },
    hide_index=True,
)


with stp.form("example_form"):
    df = stp.data_editor(
        example_df,
        url_key="example_data_editor2",
        num_rows="dynamic",
        compress=True,
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
            "birthday": st.column_config.DateColumn(
                "Birthday",
                min_value=date(1900, 1, 1),
                max_value=date(2005, 1, 1),
                format="DD.MM.YYYY",
                step=1,
            ),
            "appointment (time)": st.column_config.TimeColumn(
                "Appointment (time)",
                min_value=time(8, 0, 0),
                max_value=time(19, 0, 0),
                format="hh:mm a",
                step=60,
            ),
            "json": st.column_config.JsonColumn(
                "JSON Data",
                help="JSON strings or objects",
                width="large",
            ),
            "sales": st.column_config.ListColumn(
                "Sales (last 6 months)",
                help="The sales volume in the last 6 months",
                width="medium",
            ),
            "links": st.column_config.LinkColumn(
                "Trending apps",
                help="The top trending Streamlit apps",
                validate=r"^https://[a-z]+\.streamlit\.app$",
                max_chars=100,
                display_text=r"https://(.*?)\.streamlit\.app",
            ),
            "images": st.column_config.ImageColumn(
                "Preview Image", help="Streamlit app preview screenshots"
            ),
            "sales (area)": st.column_config.AreaChartColumn(
                "Sales (last 6 months)",
                width="medium",
                help="The sales volume in the last 6 months",
                y_min=0,
                y_max=100,
            ),
        },
        hide_index=True,
    )
    stp.form_submit_button("Submit")
