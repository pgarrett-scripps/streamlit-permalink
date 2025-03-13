import streamlit as st
import streamlit_permalink as stp
from datetime import date, datetime

# Basic date input with default value
stp.date_input("Basic Date", value=date(2024, 1, 1), url_key="date")

# Date input with min/max dates
stp.date_input("Limited Date", 
                min_value=date(2024, 1, 1),
                max_value=date(2024, 12, 31),
                value=date(2024, 6, 15),
                url_key="limited_date")

# Date range input
stp.date_input("Date Range",
                value=(date(2024, 1, 1), date(2024, 12, 31)),
                url_key="date_range")

# Date input with 'today' value
stp.date_input("Today Date", 
                value="today",
                url_key="today_date")

# Date input with datetime object
stp.date_input("Datetime Input", 
                value=datetime(2024, 5, 15, 10, 30, 0),
                url_key="datetime_date")
