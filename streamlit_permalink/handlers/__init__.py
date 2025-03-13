from .checkbox import handle_checkbox
from .toggle import handle_toggle
from .radio import handle_radio
from .selectbox import handle_selectbox
from .option_menu import handle_option_menu
from .multiselect import handle_multiselect
from .slider import handle_slider
from .select_slider import handle_select_slider
from .text_input import handle_text_input
from .number_input import handle_number_input
from .text_area import handle_text_area
from .date_input import handle_date_input
from .time_input import handle_time_input
from .color_picker import handle_color_picker
from .pills import handle_pills
from .segmented_control import handle_segmented_control


HANDLERS = {
    'checkbox': handle_checkbox,
    'toggle': handle_toggle,
    'radio': handle_radio,
    'selectbox': handle_selectbox,
    'option_menu': handle_option_menu,
    'multiselect': handle_multiselect,
    'slider': handle_slider,
    'select_slider': handle_select_slider,
    'text_input': handle_text_input,
    'number_input': handle_number_input,
    'text_area': handle_text_area,
    'date_input': handle_date_input,
    'time_input': handle_time_input,
    'color_picker': handle_color_picker,
    'pills': handle_pills,
    'segmented_control': handle_segmented_control,
}