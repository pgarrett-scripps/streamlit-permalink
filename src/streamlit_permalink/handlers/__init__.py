"""
This module contains handlers for the Streamlit widgets.
"""

from typing import Dict, Type

import streamlit as st

# Base handlers that are available in all Streamlit versions
from .checkbox import CheckboxHandler
from .color_picker import ColorPickerHandler
from .date_input import DateInputHandler
from .handler import WidgetHandler
from .multiselect import MultiSelectHandler
from .number_input import NumberInputHandler
from .radio import RadioHandler
from .selectbox import SelectboxHandler
from .slider import SliderHandler
from .text_area import TextAreaHandler
from .text_input import TextInputHandler
from .time_input import TimeInputHandler

# Initialize handlers dictionary with base widgets
HANDLERS: Dict[str, Type[WidgetHandler]] = {
    "checkbox": CheckboxHandler,
    "radio": RadioHandler,
    "selectbox": SelectboxHandler,
    "multiselect": MultiSelectHandler,
    "slider": SliderHandler,
    "text_input": TextInputHandler,
    "number_input": NumberInputHandler,
    "text_area": TextAreaHandler,
    "date_input": DateInputHandler,
    "time_input": TimeInputHandler,
    "color_picker": ColorPickerHandler,
}

# Conditionally add newer widget handlers
if hasattr(st, "toggle"):
    from .toggle import ToggleHandler

    HANDLERS["toggle"] = ToggleHandler

if hasattr(st, "select_slider"):
    from .select_slider import SelectSliderHandler

    HANDLERS["select_slider"] = SelectSliderHandler

if hasattr(st, "pills"):
    from .pills import PillsHandler

    HANDLERS["pills"] = PillsHandler

if hasattr(st, "segmented_control"):
    from .segmented_control import SegmentedControlHandler

    HANDLERS["segmented_control"] = SegmentedControlHandler

if hasattr(st, "data_editor"):
    from .data_editor import DataEditorHandler

    HANDLERS["data_editor"] = DataEditorHandler

# option menu (from streamlit_option_menu import option_menu) not in st
try:
    from streamlit_option_menu import option_menu  # type: ignore

    from .option_menu import OptionMenuHandler

    HANDLERS["option_menu"] = OptionMenuHandler
except ImportError:
    pass
