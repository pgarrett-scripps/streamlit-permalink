"""
This module contains handlers for the Streamlit widgets.
"""

import streamlit as st

# Base handlers that are available in all Streamlit versions
from .checkbox import handle_checkbox
from .radio import handle_radio
from .selectbox import handle_selectbox
from .multiselect import handle_multiselect
from .slider import handle_slider
from .text_input import handle_text_input
from .number_input import handle_number_input
from .text_area import handle_text_area
from .date_input import handle_date_input
from .time_input import handle_time_input
from .color_picker import handle_color_picker

# Initialize handlers dictionary with base widgets
HANDLERS = {
    "checkbox": handle_checkbox,
    "radio": handle_radio,
    "selectbox": handle_selectbox,
    "multiselect": handle_multiselect,
    "slider": handle_slider,
    "text_input": handle_text_input,
    "number_input": handle_number_input,
    "text_area": handle_text_area,
    "date_input": handle_date_input,
    "time_input": handle_time_input,
    "color_picker": handle_color_picker,
}

# Conditionally add newer widget handlers
if hasattr(st, "toggle"):
    from .toggle import handle_toggle

    HANDLERS["toggle"] = handle_toggle

if hasattr(st, "select_slider"):
    from .select_slider import handle_select_slider

    HANDLERS["select_slider"] = handle_select_slider

if hasattr(st, "option_menu"):
    from .option_menu import handle_option_menu

    HANDLERS["option_menu"] = handle_option_menu

if hasattr(st, "pills"):
    from .pills import handle_pills

    HANDLERS["pills"] = handle_pills

if hasattr(st, "segmented_control"):
    from .segmented_control import handle_segmented_control

    HANDLERS["segmented_control"] = handle_segmented_control

if hasattr(st, "data_editor"):
    from .data_editor import handle_data_editor

    HANDLERS["data_editor"] = handle_data_editor

# option menu (from streamlit_option_menu import option_menu) not in st
try:
    from streamlit_option_menu import option_menu
    from .option_menu import handle_option_menu

    HANDLERS["option_menu"] = handle_option_menu
except ImportError:
    pass
