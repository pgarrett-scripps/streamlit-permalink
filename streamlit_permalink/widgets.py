import streamlit as st
from packaging.version import parse as V
from typing import Callable, Any, Dict, Optional, Type, TypeVar
from .utils import to_url_value
from .core import form_state
from .handlers import HANDLERS
import inspect

T = TypeVar('T')

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
    def __get__(self, form: 'UrlAwareForm', _objtype: Optional[Type] = None) -> 'UrlAwareWidget':
        """Implements the descriptor protocol for form-based widget access."""
        assert isinstance(form, UrlAwareForm)
        return UrlAwareWidget(getattr(form.base_form, self.base_widget.__name__), form)
    
    def __call__(self, *args, **kwargs):

        url_key = kwargs.pop('url_key', None)

        signature = inspect.signature(self.base_widget)
        bound_args = signature.bind_partial(*args, **kwargs)

        key = bound_args.arguments.get('key', None)

        # sets url key or errors 
        if url_key is None:

            if key is None:
                raise ValueError("url_key or key is required")
            else:
                url_key = key

        if key is None:
            bound_args.arguments['key'] = url_key

        active_form = form_state.get_active_form()
        if active_form is not None:
            return self.call_inside_form(active_form, url_key, bound_args)
        
        if V(st.__version__) < V('1.30'):
            url = st.experimental_get_query_params()

        # if user provides on_change and its not None, we need to update the url when the widget changes
        if 'on_change' in kwargs and kwargs['on_change'] is not None:
            user_supplied_change_handler = kwargs.get('on_change', lambda *args, **kwargs: None)
        else:
            user_supplied_change_handler = None

        def on_change(*args, **kwargs):
            if V(st.__version__) < V('1.30'):
                url[url_key] = to_url_value(getattr(st.session_state, bound_args.arguments['key']))
                st.experimental_set_query_params(**url)
            else:
                st.query_params[url_key] = to_url_value(getattr(st.session_state, bound_args.arguments['key']))

            if user_supplied_change_handler is not None:
                user_supplied_change_handler(*args, **kwargs)

        bound_args.arguments['on_change'] = on_change
        if V(st.__version__) < V('1.30'):
            url_value = url.get(url_key, None)
        else:
            url_value = st.query_params.get_all(url_key) or None

        handler = HANDLERS[self.base_widget.__name__]
        result = handler(url_key, url_value, bound_args)
        return result

    def call_inside_form(self, form, url_key, bound_args):

        form.field_mapping[url_key] = bound_args.arguments['key']

        if V(st.__version__) < V('1.30'):
            url = st.experimental_get_query_params()
            url_value = url.get(url_key, None)
        else:
            url_value = st.query_params.get_all(url_key) or None
            
        handler = HANDLERS[self.base_widget.__name__]
        result = handler(url_key, url_value, bound_args)
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
    def __get__(self, form: 'UrlAwareForm', _objtype: Optional[Type] = None) -> 'UrlAwareFormSubmitButton':
        """Implements the descriptor protocol for form-based button access."""
        assert isinstance(form, UrlAwareForm)
        return UrlAwareFormSubmitButton(getattr(form.base_form, self.base_widget.__name__), form)

    def __call__(self, *args, **kwargs):
        active_form = form_state.get_active_form()
        if active_form is not None:
            return self.call_inside_form(active_form, *args, **kwargs)
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

    def __init__(self, key: str, *args: Any, **kwargs: Any) -> None:
        self.base_form = st.form(key, *args, **kwargs)
        # map from URL query param names to streamlit widget keys
        self.field_mapping: Dict[str, str] = {}

    def __enter__(self):
        self.base_form.__enter__()
        # Use the context manager instead of directly setting global variable
        self._form_context = form_state.set_active_form(self)
        self._form_context.__enter__()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        # Exit the context manager to restore previous state
        self._form_context.__exit__(exc_type, exc_val, exc_tb)
        return self.base_form.__exit__(exc_type, exc_val, exc_tb)

    def __getattr__(self, attr: str) -> Any:
        """Delegates attribute access to the underlying form."""
        return getattr(self.base_form, attr)


form = UrlAwareForm
