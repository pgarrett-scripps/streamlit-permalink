from functools import partial
import streamlit as st
from packaging.version import parse as V
from typing import Callable, Any, Dict, List, Optional, Type, TypeVar, Union
from .utils import compress_text, decompress_text, to_url_value
#from .core import form_state
from .handlers import HANDLERS
from .constants import _EMPTY, _NONE
import inspect
from streamlit.delta_generator import DeltaGenerator

_active_form = None

T = TypeVar('T')

# write a function that takes a callable and a list and runs it with each element of the list
def _compress_list(func: Callable, l: Union[List[str], str]):
    if isinstance(l, str):
        return func(l)
    if isinstance(l, (list, tuple)):
        return [func(e) for e in l]
    
def _decompress_list(func: Callable, l: List[str]):
    l = [func(e) for e in l]

    if l == [_EMPTY]:
        return []
    
    if l == [_NONE]:
        return None
    
    return l



class UrlAwareWidget:
    """A wrapper class that adds URL parameter awareness to Streamlit widgets.
    
    This class wraps standard Streamlit widgets to enable their values to be 
    controlled via URL parameters, enabling permalink functionality.
    
    Args:
        base_widget (Callable): The original Streamlit widget function to wrap
        form (Optional[UrlAwareForm]): The form instance if this widget is part of a form
    """
    def __init__(self, base_widget: Callable, form: Optional['UrlAwareForm'] = None) -> None:
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

        url_key = kwargs.pop('url_key', None)
        compress = kwargs.pop('compress', False)
        compressor = kwargs.pop('compressor', compress_text)
        decompressor = kwargs.pop('decompressor', decompress_text)
        stateful = kwargs.pop('stateful', True)

        if stateful is False:
            return self.base_widget(*args, **kwargs)

        if not compress:
            compressor = lambda x: x
            decompressor = lambda x: x

        #partial partial run_with_each_element for compressor and decompressor
        compressor = partial(_compress_list, compressor)
        decompressor = partial(_decompress_list, decompressor)

        signature = inspect.signature(self.base_widget)
        bound_args = signature.bind_partial(*args, **kwargs)

        key = bound_args.arguments.get('key', None)

        # sets url key or errors 
        if url_key is None:
            if key is not None:
                url_key = key
            elif bound_args.arguments.get('label') is not None:
                url_key = bound_args.arguments['label']
            else:
                raise ValueError("url_key or key is required")

        bound_args.arguments['key'] = url_key

        if _active_form is not None or self.form is not None:
            return self.call_inside_form(self.form or _active_form, url_key, bound_args, compressor=compressor, decompressor=decompressor)
        
        if V(st.__version__) < V('1.30'):
            url = st.experimental_get_query_params()

        # if user provides on_change and its not None, we need to update the url when the widget changes
        user_supplied_change_handler = None
        if 'on_change' in bound_args.arguments and bound_args.arguments['on_change'] is not None:
            user_supplied_change_handler = bound_args.arguments.get('on_change')

        def on_change(*args, **kwargs):

            if V(st.__version__) < V('1.30'):
                url[url_key] = compressor(to_url_value(getattr(st.session_state, bound_args.arguments['key'])))
                st.experimental_set_query_params(**url)
            else:
                st.query_params[url_key] = compressor(to_url_value(getattr(st.session_state, bound_args.arguments['key'])))

            if user_supplied_change_handler is not None:
                user_supplied_change_handler(*args, **kwargs)

        bound_args.arguments['on_change'] = on_change
        if V(st.__version__) < V('1.30'):
            url_value = url.get(url_key, None)
        else:
            url_value = st.query_params.get_all(url_key) or None

        handler = HANDLERS[self.base_widget.__name__]
        result = handler(self.base_widget, url_key, url_value, bound_args, compressor=compressor, decompressor=decompressor)
        return result

    def call_inside_form(self, form, url_key, bound_args, compressor, decompressor):

        form.field_mapping[url_key] = bound_args.arguments['key']

        if V(st.__version__) < V('1.30'):
            url = st.experimental_get_query_params()
            url_value = url.get(url_key, None)
        else:
            url_value = st.query_params.get_all(url_key) or None
            
        handler = HANDLERS[self.base_widget.__name__]
        result = handler(self.base_widget, url_key, url_value, bound_args, compressor=compressor, decompressor=decompressor)
        return result


class UrlAwareFormSubmitButton:
    """A wrapper class for Streamlit form submit buttons with URL parameter support.
    
    Handles updating URL parameters when a form is submitted.
    
    Args:
        base_widget (Callable): The original form submit button widget
        form (Optional[UrlAwareForm]): The form instance if this button is part of a form
    """
    def __init__(self, base_widget: Callable, form: Optional['UrlAwareForm'] = None) -> None:
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
    """A wrapper class for Streamlit forms that adds URL parameter support.
    
    Enables form fields to be controlled via URL parameters and updates the URL
    when the form is submitted.
    
    Args:
        key (str): The unique key for the form
        *args: Additional positional arguments passed to st.form
        **kwargs: Additional keyword arguments passed to st.form
    """
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

def __getattr__(name: str) -> Any:
    try:
        return getattr(st, name)
    except AttributeError as e:
        raise AttributeError(str(e).replace('streamlit', 'streamlit_permalink')) 