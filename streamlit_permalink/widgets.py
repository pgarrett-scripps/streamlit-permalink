from datetime import datetime
import streamlit as st
from packaging.version import parse as V
from .utils import to_url_value, _EMPTY
from .core import _active_form
from .handlers import HANDLERS

class UrlAwareWidget:
    def __init__(self, base_widget, form=None):
        self.base_widget = base_widget
        self.form = form
        self.__module__ = base_widget.__module__
        self.__name__ = base_widget.__name__
        self.__qualname__ = base_widget.__qualname__
        self.__doc__ = base_widget.__doc__
        self.__annotations__ = base_widget.__annotations__

    # Widgets inside forms in Streamlit can be created in 2 ways:
    #   form = st.form('my_form')
    #   with form:
    #       st.text_input(...)  # first way
    #   form.text_input(...)    # second, equivalent way
    # For this second way, we need to know if UrlAwareWidget has been
    # called like a method on the form object. Therefore, we use the
    # descriptor protocol to attach the form object:
    def __get__(self, form, _objtype=None):
        assert isinstance(form, UrlAwareForm)
        return UrlAwareWidget(getattr(form.base_form, self.base_widget.__name__), form)

    def __call__(self, *args, **kwargs):
        if 'url_key' not in kwargs:
            return self.base_widget(*args, **kwargs)
        if _active_form is not None or self.form is not None:
            return self.call_inside_form(self.form or _active_form, *args, **kwargs)
        url_key = kwargs.pop('url_key')
        if 'key' not in kwargs:
            kwargs['key'] = url_key
        key = kwargs['key']
        if V(st.__version__) < V('1.30'):
            url = st.experimental_get_query_params()
        user_supplied_change_handler = kwargs.get('on_change', lambda *args, **kwargs: None)

        def on_change(*args, **kwargs):
            if V(st.__version__) < V('1.30'):
                url[url_key] = to_url_value(getattr(st.session_state, key))
                st.experimental_set_query_params(**url)
            else:
                st.query_params[url_key] = to_url_value(getattr(st.session_state, key))
            user_supplied_change_handler(*args, **kwargs)


        kwargs['on_change'] = on_change
        if V(st.__version__) < V('1.30'):
            url_value = url.get(url_key, None)
        else:
            url_value = st.query_params.get_all(url_key) or None
        handler = HANDLERS[self.base_widget.__name__]
        # TODO: remove the first return value from the handle_{widget-name}() methods
        # NOTE: do this when we gain confidence that the on_change callbacks are a
        # reliable replacement for the SessionState-based hacky solution for permalinks
        _, result = handler(self.base_widget, url_value, *args, **kwargs)

        return result

    def call_inside_form(self, form, *args, **kwargs):
        url_key = kwargs.pop('url_key')
        if 'key' not in kwargs:
            kwargs['key'] = url_key
        key = kwargs['key']
        form.field_mapping[url_key] = key
        if V(st.__version__) < V('1.30'):
            url = st.experimental_get_query_params()
            url_value = url.get(url_key, None)
        else:
            url_value = st.query_params.get_all(url_key) or None
        handler = getattr(self, f'handle_{self.base_widget.__name__}')
        _, result = handler(url_value, *args, **kwargs)
        return result


class UrlAwareFormSubmitButton:
    def __init__(self, base_widget, form=None):
        self.base_widget = base_widget
        self.form = form

    # Widgets inside forms in Streamlit can be created in 2 ways:
    #   form = st.form('my_form')
    #   with form:
    #       st.text_input(...)  # first way
    #   form.text_input(...)    # second, equivalent way
    # For this second way, we need to know if UrlAwareWidget has been
    # called like a method on the form object. Therefore, we use the
    # descriptor protocol to attach the form object:
    def __get__(self, form, _objtype=None):
        assert isinstance(form, UrlAwareForm)
        return UrlAwareFormSubmitButton(getattr(form.base_form, self.base_widget.__name__), form)

    def __call__(self, *args, **kwargs):
        if _active_form is not None or self.form is not None:
            return self.call_inside_form(self.form or _active_form, *args, **kwargs)
        return self.base_widget(*args, **kwargs)

    def call_inside_form(self, form, *args, **kwargs):
        if V(st.__version__) < V('1.30'):
            url = st.experimental_get_query_params()
        user_supplied_click_handler = kwargs.get('on_click', lambda: None)

        def on_click(*args, **kwargs):
            for url_key, key in form.field_mapping.items():
                raw_value = getattr(st.session_state, key)
                if raw_value is not None:
                    if V(st.__version__) < V('1.30'):
                        url[url_key] = to_url_value(raw_value)
                    else:
                        st.query_params[url_key] = to_url_value(raw_value)
            if V(st.__version__) < V('1.30'):
                st.experimental_set_query_params(**url)
            user_supplied_click_handler(*args, **kwargs)

        kwargs['on_click'] = on_click
        return self.base_widget(*args, **kwargs)


checkbox = UrlAwareWidget(st.checkbox)
if hasattr(st, 'toggle'):
    toggle = UrlAwareWidget(st.toggle)
radio = UrlAwareWidget(st.radio)
selectbox = UrlAwareWidget(st.selectbox)
multiselect = UrlAwareWidget(st.multiselect)
slider = UrlAwareWidget(st.slider)
select_slider = UrlAwareWidget(st.select_slider)
text_input = UrlAwareWidget(st.text_input)
number_input = UrlAwareWidget(st.number_input)
text_area = UrlAwareWidget(st.text_area)
date_input = UrlAwareWidget(st.date_input)
time_input = UrlAwareWidget(st.time_input)
color_picker = UrlAwareWidget(st.color_picker)
if hasattr(st, 'pills'):
    pills = UrlAwareWidget(st.pills)
if hasattr(st, 'feedback'):
    feedback = UrlAwareWidget(st.feedback)
if hasattr(st, 'segmented_control'):
    segmented_control = UrlAwareWidget(st.segmented_control)
form_submit_button = UrlAwareFormSubmitButton(st.form_submit_button)

try:
    import streamlit_option_menu
    option_menu = UrlAwareWidget(streamlit_option_menu.option_menu)
    _has_option_menu = True
except ImportError:
    _has_option_menu = False


class UrlAwareForm:
    checkbox = UrlAwareWidget(st.checkbox)
    if hasattr(st, 'toggle'):
        toggle = UrlAwareWidget(st.toggle)
    radio = UrlAwareWidget(st.radio)
    selectbox = UrlAwareWidget(st.selectbox)
    multiselect = UrlAwareWidget(st.multiselect)
    slider = UrlAwareWidget(st.slider)
    select_slider = UrlAwareWidget(st.select_slider)
    text_input = UrlAwareWidget(st.text_input)
    number_input = UrlAwareWidget(st.number_input)
    text_area = UrlAwareWidget(st.text_area)
    date_input = UrlAwareWidget(st.date_input)
    time_input = UrlAwareWidget(st.time_input)
    color_picker = UrlAwareWidget(st.color_picker)
    if hasattr(st, 'pills'):
        pills = UrlAwareWidget(st.pills)
    if hasattr(st, 'feedback'):
        feedback = UrlAwareWidget(st.feedback)
    if hasattr(st, 'segmented_control'):
        segmented_control = UrlAwareWidget(st.segmented_control)
    form_submit_button = UrlAwareFormSubmitButton(st.form_submit_button)

    if _has_option_menu:
        option_menu = UrlAwareWidget(streamlit_option_menu.option_menu)

    def __init__(self, key, *args, **kwargs):
        self.base_form = st.form(key, *args, **kwargs)
        # map from URL query param names to streamlit widget keys
        self.field_mapping = {}

    def __enter__(self):
        global _active_form
        _active_form = self
        return self.base_form.__enter__()

    def __exit__(self, exc_type, exc_value, traceback):
        global _active_form
        _active_form = None
        return self.base_form.__exit__(exc_type, exc_value, traceback)

    def __getattr__(self, attr):
        return getattr(self.base_form, attr)


form = UrlAwareForm
