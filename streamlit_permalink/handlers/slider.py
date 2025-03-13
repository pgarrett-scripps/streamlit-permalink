from datetime import datetime, date, time
from enum import Enum
from typing import List, Optional, Union

import inspect
from datetime import timedelta
import streamlit as st

from ..utils import init_url_value
from ..exceptions import UrlParamError

class SliderType(Enum):
    SINGLE_INT = "single-int"
    SINGLE_FLOAT = "single-float"
    SINGLE_DATETIME = "single-datetime"
    SINGLE_DATE = "single-date"
    SINGLE_TIME = "single-time"
    MULTI_INT = "multi-int"
    MULTI_FLOAT = "multi-float"
    MULTI_DATETIME = "multi-datetime"
    MULTI_DATE = "multi-date"
    MULTI_TIME = "multi-time"

    
def _get_defaults(min_value: Union[int, float, datetime, date, time, None], 
                  max_value: Union[int, float, datetime, date, time, None], 
                  value: Union[int, float, datetime, date, time, list, tuple, None],
                  step: Union[int, float, timedelta, None]):
    # this function verifys min. max, value, and step are correct types and values, and initializes them if needed
    
    # If min and value are provided, then use them (but verify bounds)
    # if only min is provided then set value=min
    # if only value is provided and is type date, then set min=value-timedelta(14days)
    # if only value is provided and is type datetime, then set min=value-timedelta(14days)
    # if only value is provided and is type time, then set min=time.min
    # if only value is provided and is type int, then set min=min(val, 0)
    # if only value is provided and is type float, then set min=min(val, 0.0)
    # if only value is provided and is type list, then set min=min(val[0], 0)
    # if only value is provided and is type tuple, then set min=min(val[0], 0)
    # if both min and value are none, then set min=0, and value=0

    slider_type = _get_slider_type(min_value, max_value, value, step)

    # handle min and value
    if min_value is not None and value is None:
        value = min_value
    elif value is not None and min_value is None:
        if isinstance(value, (list, tuple)):
            _value = value[0]
        else:
            _value = value
        if slider_type == SliderType.SINGLE_DATE or slider_type == SliderType.MULTI_DATE:
            min_value = _value - timedelta(days=14)
        elif slider_type == SliderType.SINGLE_DATETIME or slider_type == SliderType.MULTI_DATETIME:
            min_value = _value - timedelta(days=14)
        elif slider_type == SliderType.SINGLE_TIME or slider_type == SliderType.MULTI_TIME:
            min_value = time.min
        elif slider_type == SliderType.SINGLE_INT or slider_type == SliderType.MULTI_INT:
            min_value = min(_value, 0)
        elif slider_type == SliderType.SINGLE_FLOAT or slider_type == SliderType.MULTI_FLOAT:
            min_value = min(_value, 0.0)
        else:
            raise ValueError(f"Unsupported slider type: {slider_type}")
    elif min_value is None and value is None:
        min_value = 0
        value = 0
        
    # Now min and value are set

    # handle max
    if max_value is None:

        if isinstance(value, (list, tuple)):
            _value = value[0]
        else:
            _value = value
    
        if slider_type == SliderType.SINGLE_DATE or slider_type == SliderType.MULTI_DATE:
            max_value = _value + timedelta(days=14)
        elif slider_type == SliderType.SINGLE_DATETIME or slider_type == SliderType.MULTI_DATETIME:
            max_value = _value + timedelta(days=14)
        elif slider_type == SliderType.SINGLE_TIME or slider_type == SliderType.MULTI_TIME:
            max_value = time.max
        elif slider_type == SliderType.SINGLE_INT or slider_type == SliderType.MULTI_INT:
            max_value = max(_value, 100)
        elif slider_type == SliderType.SINGLE_FLOAT or slider_type == SliderType.MULTI_FLOAT:
            max_value = max(_value, 1.0)
        else:
            raise ValueError(f"Unsupported slider type: {slider_type}")
        
    # Now min and max and value are set, validate step
    # The stepping interval. Defaults to 1 if the value is an int, 0.01 if a float, 
    # timedelta(days=1) if a date/datetime, timedelta(minutes=15) if a time (or if max_value - min_value < 1 day)
    if step is None:
        if slider_type == SliderType.SINGLE_INT or slider_type == SliderType.MULTI_INT:
            step = 1
        elif slider_type == SliderType.SINGLE_FLOAT or slider_type == SliderType.MULTI_FLOAT:
            step = 0.01
        elif slider_type == SliderType.SINGLE_DATE or slider_type == SliderType.MULTI_DATE:
            step = timedelta(days=1)
        elif slider_type == SliderType.SINGLE_DATETIME or slider_type == SliderType.MULTI_DATETIME:
            if max_value - min_value < timedelta(days=1):
                step = timedelta(minutes=15)
            else:
                step = timedelta(days=1)
        elif slider_type == SliderType.SINGLE_TIME or slider_type == SliderType.MULTI_TIME:
            step = timedelta(minutes=15)
        else:
            raise ValueError(f"Unsupported slider type: {slider_type}")
        
    return min_value, max_value, value, step, slider_type
        
        

def _validate_step(step: Union[int, float, timedelta, None], slider_type: SliderType):
    if step is not None:
        if slider_type == SliderType.SINGLE_INT or slider_type == SliderType.MULTI_INT:
            if not isinstance(step, int):
                raise ValueError(f"Step must be an integer for single or multi int slider: {step}")
        elif slider_type == SliderType.SINGLE_FLOAT or slider_type == SliderType.MULTI_FLOAT:
            if not isinstance(step, float):
                raise ValueError(f"Step must be a float for single or multi float slider: {step}")
        elif slider_type == SliderType.SINGLE_DATETIME or slider_type == SliderType.MULTI_DATETIME:
            if not isinstance(step, timedelta):
                raise ValueError(f"Step must be a timedelta for single or multi datetime slider: {step}")
        elif slider_type == SliderType.SINGLE_DATE or slider_type == SliderType.MULTI_DATE:
            if not isinstance(step, timedelta):
                raise ValueError(f"Step must be a timedelta for single or multi date slider: {step}")
        elif slider_type == SliderType.SINGLE_TIME or slider_type == SliderType.MULTI_TIME:
            if not isinstance(step, timedelta):
                raise ValueError(f"Step must be a timedelta for single or multi time slider: {step}")
        else:
            raise ValueError(f"Step is not supported for slider type: {slider_type}")

def _get_slider_type(min_value: Union[int, float, datetime, date, time, None], 
                     max_value: Union[int, float, datetime, date, time, None], 
                     value: Union[int, float, datetime, date, time, None, list, tuple], 
                     step: Union[int, float, timedelta, None]) -> SliderType:

    option_types = {type(min_value), type(max_value)}
    if isinstance(value, (list, tuple)):

        if len(value) != 2:
            raise ValueError(f"Invalid value for slider parameter: {value}. Expected a list or tuple of length 2.")

        for v in value:
            option_types.add(type(v))
    else:
        option_types.add(type(value))

    # remove None from option_types
    option_types = {t for t in option_types if t is not type(None)}

    if len(option_types) == 0:
        slider_type = SliderType.SINGLE_INT # default to single int
    elif len(option_types) == 1:
        option_type = option_types.pop()
        if isinstance(value, (list, tuple)):
            if option_type == int:
                slider_type = SliderType.MULTI_INT
            elif option_type == float:
                slider_type = SliderType.MULTI_FLOAT
            elif option_type == datetime:
                slider_type = SliderType.MULTI_DATETIME
            elif option_type == date:
                slider_type = SliderType.MULTI_DATE
            elif option_type == time:
                slider_type = SliderType.MULTI_TIME
        elif option_type == int:
            slider_type = SliderType.SINGLE_INT
        elif option_type == float:
            slider_type = SliderType.SINGLE_FLOAT
        elif option_type == datetime:
            slider_type = SliderType.SINGLE_DATETIME
        elif option_type == date:
            slider_type = SliderType.SINGLE_DATE
        elif option_type == time:
            slider_type = SliderType.SINGLE_TIME
        else:
            raise ValueError(f"Unsupported slider type: {option_type}")
    else:
        raise ValueError(f"All slider parameters must be of the same type: {option_types}")
            
    _validate_step(step, slider_type)
    
    return slider_type

def handle_slider(url_key: str, url_value: Optional[List[str]], bound_args: inspect.BoundArguments):
    """
    Handle slider widget URL state.

    Args:
        url_key: URL parameter key
        url_value: URL parameter value(s)
        bound_args: Bound arguments for the slider widget
    """



    # Get slider parameters
    min_value = bound_args.arguments.get('min_value')
    max_value = bound_args.arguments.get('max_value')
    value = bound_args.arguments.get('value')
    step = bound_args.arguments.get('step')

    min_value, max_value, value, step, slider_type = _get_defaults(min_value, max_value, value, step)

    # if not url_value, set it to the default value
    if not url_value:
        # Determine default value based on Streamlit's default behavior
        init_url_value(url_key, value)
        return st.slider(**bound_args.arguments)

    # Determine if this is a range slider based on the initial value
    # Default to single slider if value is None
    is_multi = isinstance(value, (list, tuple))
    expected_values = 2 if is_multi else 1

    # Validate number of values matches slider type
    if len(url_value) != expected_values:
        raise UrlParamError(
            f"Invalid number of values for slider parameter '{url_key}': got {len(url_value)}, "
            f"expected {expected_values} ({'range' if is_multi else 'single'} slider)"
        )

    try:
        # Parse values based on type
        if slider_type == SliderType.SINGLE_INT or slider_type == SliderType.MULTI_INT:
            parsed_values = [int(v) for v in url_value]
        elif slider_type == SliderType.SINGLE_FLOAT or slider_type == SliderType.MULTI_FLOAT:
            parsed_values = [float(v) for v in url_value]
        elif slider_type == SliderType.SINGLE_DATE or slider_type == SliderType.MULTI_DATE:
            parsed_values = [datetime.strptime(v, '%Y-%m-%d').date() for v in url_value]
        elif slider_type == SliderType.SINGLE_DATETIME or slider_type == SliderType.MULTI_DATETIME:
            parsed_values = [datetime.strptime(v, '%Y-%m-%dT%H:%M:%S') for v in url_value]
        elif slider_type == SliderType.SINGLE_TIME or slider_type == SliderType.MULTI_TIME:
            parsed_values = [datetime.strptime(v, '%H:%M').time() for v in url_value]
        else:
            raise ValueError(f"Unsupported slider type: {slider_type}")
           

    except ValueError as e:
        raise UrlParamError(
            f"Invalid value(s) for slider parameter '{url_key}': {url_value}. "
            f"Expected {slider_type.name} value(s). Error: {str(e)}"
        )
    

    # Set single value or range based on number of values
    if is_multi == True and len(parsed_values) != 2:
        raise UrlParamError(
            f"Invalid number of values for slider parameter '{url_key}': {len(parsed_values)}. "
            "Expected 1 value for single slider or 2 values for range slider."
        )
    
    if is_multi == False and len(parsed_values) != 1:
        raise UrlParamError(
            f"Invalid number of values for slider parameter '{url_key}': {len(parsed_values)}. "
            "Expected 1 value for single slider."
        )
    
    if is_multi == True:
        if parsed_values[0] > parsed_values[1]:
            raise UrlParamError(
                f"Invalid range for slider parameter '{url_key}': "
                f"start value {parsed_values[0]} is greater than end value {parsed_values[1]}."
            )
        
        # assert that parsed_values[0] and parsed_values[1] are within the min and max values
        if parsed_values[0] < min_value or parsed_values[1] > max_value:
            raise UrlParamError(
                f"Invalid range for slider parameter '{url_key}': "
                f"range values are out of bounds."
            )
        
        bound_args.arguments['value'] = tuple(parsed_values)
        
    else:
        if parsed_values[0] < min_value or parsed_values[0] > max_value:
            raise UrlParamError(
                f"Invalid value for slider parameter '{url_key}': "
                f"value is out of bounds."
            )
    
        bound_args.arguments['value'] = parsed_values[0]

    return st.slider(**bound_args.arguments)