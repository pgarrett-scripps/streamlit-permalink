from datetime import datetime
from .utils import _EMPTY

def handle_checkbox(base_widget, url_value, label, value=False, *args, **kwargs):
    url_value = url_value and url_value[0]
    url_value = {'True': True, 'False': False}.get(url_value, url_value)
    if url_value is not None:
        value = url_value
    result = base_widget(label, value, *args, **kwargs)
    return str(result), result

def handle_toggle(base_widget, url_value, label, value=False, *args, **kwargs):
    return handle_checkbox(base_widget, url_value, label, value, *args, **kwargs)

def handle_radio(base_widget, url_value, *args, **kwargs):
    return handle_selectbox(base_widget, url_value, *args, **kwargs)

def handle_selectbox(base_widget, url_value, label, options, index=0, *args, **kwargs):
    url_value = url_value and url_value[0]
    options = list(map(str, options))
    if url_value is not None:
        try:
            index = options.index(url_value)
        except ValueError:
            pass
    result = base_widget(label, options, index, *args, **kwargs)
    return result, result

def handle_option_menu(base_widget, url_value, menu_title, options, default_index=0, *args, **kwargs):
    url_value = url_value and url_value[0]
    options = list(map(str, options))
    if url_value is not None:
        try:
            default_index = options.index(url_value)
        except ValueError:
            pass
    result = base_widget(menu_title, options, default_index, *args, **kwargs)
    return result, result

def handle_multiselect(base_widget, url_value, label, options, default=None, *args, **kwargs):
    options = list(map(str, options))
    if url_value == [_EMPTY]:
        default = []
    elif url_value is not None:
        default = url_value
    result = base_widget(label, options, default, *args, **kwargs)
    return result, result

def handle_slider(base_widget, url_value, label, min_value=None, max_value=None, value=None, *args, **kwargs):
    if value is not None and not isinstance(value, list):
        slider_type = type(value)
    if value is not None and isinstance(value, list):
        slider_type = type(value[0])
    elif min_value is not None:
        slider_type = type(min_value)
    elif max_value is not None:
        slider_type = type(max_value)
    assert slider_type in (int, float), "unsupported slider type"
    if url_value is not None:
        if len(url_value) == 1:
            value = slider_type(float(url_value[0]))
        else:
            value = [slider_type(float(i)) for i in url_value]
    result = base_widget(label, min_value, max_value, value, *args, **kwargs)
    if isinstance(result, tuple):
        new_url_value = list(map(str, result))
    else:
        new_url_value = str(result)
    return new_url_value, result

def handle_select_slider(base_widget, url_value, label, options, value=None, *args, **kwargs):
    options = list(map(str, options))
    if url_value is not None:
        if len(url_value) == 1:
            value = url_value[0]
        else:
            value = url_value
    result = base_widget(label, options, value, *args, **kwargs)
    return result, result

def handle_text_input(base_widget, url_value, label, value="", *args, **kwargs):
    if url_value is not None:
        value = url_value[0]
    result = base_widget(label, value, *args, **kwargs)
    return result, result

def handle_number_input(base_widget, url_value, label, min_value=None, max_value=None, value=None, *args, **kwargs):
    input_type = float
    if value is not None:
        input_type = type(value)
    elif min_value is not None:
        input_type = type(min_value)
    elif max_value is not None:
        input_type = type(max_value)
    assert input_type in (int, float), "unsupported number_input type"
    if url_value is not None:
        value = input_type(float(url_value[0]))
    if value is None:
        result = base_widget(label, min_value, max_value, *args, **kwargs)
    else:
        result = base_widget(label, min_value, max_value, value, *args, **kwargs)
    return str(result), result

def handle_text_area(base_widget, url_value, *args, **kwargs):
    return handle_text_input(base_widget, url_value, *args, **kwargs)

def handle_date_input(base_widget, url_value, label, value=None, *args, **kwargs):
    parse_date = lambda s: datetime.strptime(s,'%Y-%m-%d').date()
    if url_value is not None:
        if len(url_value) == 1:
            value = parse_date(url_value[0])
        else:
            value = list(map(parse_date, url_value))
    result = base_widget(label, value, *args, **kwargs)
    if isinstance(result, tuple):
        new_url_value = [d.isoformat() for d in result]
    elif result is not None:
        new_url_value = result.isoformat()
    else:
        new_url_value = result
    return new_url_value, result

def handle_time_input(base_widget, url_value, label, value=None, *args, **kwargs):
    parse_time = lambda s: datetime.strptime(s, '%H:%M').time()
    if url_value is not None:
        value = parse_time(url_value[0])
    result = base_widget(label, value, *args, **kwargs)
    if result is not None:
        return result.strftime('%H:%M'), result
    else:
        return result, result

def handle_color_picker(base_widget, url_value, label, value=None, *args, **kwargs):
    if url_value is not None:
        value = url_value[0]
    result = base_widget(label, value, *args, **kwargs)
    return result, result

def handle_pills(base_widget, url_value, label, options, selection_mode="single", default=None, *args, **kwargs):
    options = list(map(str, options))
    if selection_mode == "single":
        if url_value is not None:
            try:
                default = url_value[0]
            except (IndexError, ValueError):
                pass
        result = base_widget(label, options, selection_mode=selection_mode, default=default, *args, **kwargs)
        return result, result
    else:  # multi selection mode
        if url_value == [_EMPTY]:
            default = []
        elif url_value is not None:
            default = url_value
        result = base_widget(label, options, selection_mode=selection_mode, default=default, *args, **kwargs)
        return result, result

def handle_feedback(base_widget, url_value, options="thumbs", *args, **kwargs):
    if url_value is not None:
        if url_value[0] == "None":
            value = None
        else:
            value = int(url_value[0])
        result = base_widget(options, *args, **kwargs)
        return str(result) if result is not None else "None", result
    result = base_widget(options, *args, **kwargs)
    return str(result) if result is not None else "None", result

def handle_segmented_control(base_widget, url_value, label, options, selection_mode="single", default=None, *args, **kwargs):
    options = list(map(str, options))
    if selection_mode == "single":
        if url_value is not None:
            try:
                default = url_value[0]
            except (IndexError, ValueError):
                pass
        result = base_widget(label, options, selection_mode=selection_mode, default=default, *args, **kwargs)
        return result, result
    else:  # multi selection mode
        if url_value == [_EMPTY]:
            default = []
        elif url_value is not None:
            default = url_value
        result = base_widget(label, options, selection_mode=selection_mode, default=default, *args, **kwargs)
        return result, result


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
    'feedback': handle_feedback,
    'segmented_control': handle_segmented_control,
}

