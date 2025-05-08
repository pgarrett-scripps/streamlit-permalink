"""
This module contains handlers for the Streamlit widgets.
"""

import streamlit as st

# Base handlers that are available in all Streamlit versions
from .checkbox import HandlerCheckbox
from .radio import HandlerRadio
from .selectbox import HandlerSelectbox
from .multiselect import HandlerMultiSelect
from .slider import HandlerSlider
from .text_input import HandlerTextInput
from .number_input import HandlerNumberInput
from .text_area import HandlerTextArea
from .date_input import HandlerDateInput
from .time_input import HandlerTimeInput
from .color_picker import HandlerColorPicker

# Initialize handlers dictionary with base widgets
HANDLERS = {
    "checkbox": HandlerCheckbox,
    "radio": HandlerRadio,
    "selectbox": HandlerSelectbox,
    "multiselect": HandlerMultiSelect,
    "slider": HandlerSlider,
    "text_input": HandlerTextInput,
    "number_input": HandlerNumberInput,
    "text_area": HandlerTextArea,
    "date_input": HandlerDateInput,
    "time_input": HandlerTimeInput,
    "color_picker": HandlerColorPicker,
}

# Conditionally add newer widget handlers
if hasattr(st, "toggle"):
    from .toggle import HandlerToggle

    HANDLERS["toggle"] = HandlerToggle

if hasattr(st, "select_slider"):
    from .select_slider import HandlerSelectSlider

    HANDLERS["select_slider"] = HandlerSelectSlider

if hasattr(st, "pills"):
    from .pills import HandlerPills

    HANDLERS["pills"] = HandlerPills

if hasattr(st, "segmented_control"):
    from .segmented_control import HandlerSegmentedControl

    HANDLERS["segmented_control"] = HandlerSegmentedControl

if hasattr(st, "data_editor"):
    from .data_editor import HandlerDataEditor

    HANDLERS["data_editor"] = HandlerDataEditor

# option menu (from streamlit_option_menu import option_menu) not in st
try:
    from streamlit_option_menu import option_menu
    from .option_menu import HandlerOptionMenu

    HANDLERS["option_menu"] = HandlerOptionMenu
except ImportError:
    pass
