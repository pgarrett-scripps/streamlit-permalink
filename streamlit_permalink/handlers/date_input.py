from typing import Any, Callable, Dict, List, Optional, Union, Tuple
import inspect
import streamlit as st
from datetime import datetime, date, timedelta

from ..constants import _EMPTY, _NONE
from ..utils import init_url_value, to_url_value
from ..exceptions import UrlParamError

_DEFAULT_MIN_VALUE, _DEFAULT_MAX_VALUE = None, None
TEN_YEAR_DELTA = timedelta(days=365*10)
_HANDLER_NAME = 'date_input'
_DEFAULT_VALUE = 'today'

DateValue = Union[None, date, Tuple[date, ...]]

# Date input format examples:
# Multiple date inputs:
# (datetime.date(2024, 1, 5), datetime.date(2024, 1, 19)) -> tuple[date, date]
# (datetime.date(2024, 1, 5),) -> tuple[date]
# () -> Tuple[None]
#
# Single date input:
# datetime.date(2024, 1, 5) -> date
# None -> None

def get_today() -> date:
    """Get the current date."""
    return date.today()

def _parse_date_from_string(value: str) -> date:
    """Convert ISO format string to date object."""
    try:
        return date.fromisoformat(value)
    except ValueError:
        raise ValueError(f"Invalid date format: '{value}'. Please use YYYY-MM-DD format.")

def _parse_date_input_value(value: Any) -> Optional[date]:
    """Parse various input formats into a date object."""
    if value is None:
        return None
    elif value == "today":
        return get_today()
    elif isinstance(value, str):
        return _parse_date_from_string(value)
    elif isinstance(value, (date, datetime)):
        return value.date() if isinstance(value, datetime) else value
    else:
        raise ValueError(f"Invalid date value: {value}. Expected a date object, 'today', or a string in YYYY-MM-DD format.")

def _parse_url_date_params(url_key: str, url_value: Optional[List[str]], is_range: bool) -> DateValue:
    """Parse and validate date values from URL parameters."""
    if not is_range:

        if url_value is None:
            return None
        
        elif isinstance(url_value, list) and len(url_value) == 0:
            return None

        elif isinstance(url_value, list) and len(url_value) == 1:
            return _parse_date_from_string(url_value[0])

        else:
            raise UrlParamError(f"URL parameter '{url_key}' has {len(url_value)} values, but single date input expects exactly 1 value.")
    else: # is range
        if url_value is None:
            return ()
        
        elif isinstance(url_value, list) and len(url_value) == 0:
            return ()
        
        elif isinstance(url_value, list) and len(url_value) == 1:
            return (_parse_date_from_string(url_value[0]),)
        
        elif isinstance(url_value, list) and len(url_value) == 2:
            start, end = _parse_date_from_string(url_value[0]), _parse_date_from_string(url_value[1])

            # ensure start is before end
            if start > end:
                raise UrlParamError(f"Start date ({start}) is after end date ({end}).")

            return (start, end)

        else:
            raise UrlParamError(f"URL parameter '{url_key}' has {len(url_value)} values, but date range input expects 1 or 2 values.")


def _check_date_bounds(url_key: str, value: DateValue, min_value: date, max_value: date) -> None:
    """Check if dates are within the allowed range. Raises UrlParamError if not."""
    if value is None:
        return
    
    elif isinstance(value, date):
        if min_value is not None and value < min_value:
            raise UrlParamError(f"Date '{value}' in URL parameter '{url_key}' is before the minimum allowed date ({min_value}).")
        if max_value is not None and value > max_value:
            raise UrlParamError(f"Date '{value}' in URL parameter '{url_key}' is after the maximum allowed date ({max_value}).")
    
    elif isinstance(value, tuple):
        for i, v in enumerate(value):
            position = "start" if i == 0 else "end"
            if min_value is not None and v < min_value:
                raise UrlParamError(f"The {position} date '{v}' in URL parameter '{url_key}' is before the minimum allowed date ({min_value}).")
            if max_value is not None and v > max_value:
                raise UrlParamError(f"The {position} date '{v}' in URL parameter '{url_key}' is after the maximum allowed date ({max_value}).")

def _calculate_min_max_dates(value: Any, min_value: Optional[date], max_value: Optional[date], is_range: bool) -> Tuple[date, date]:
    """Calculate default min and max values if not provided."""
    if min_value is None:
        min_value = get_today() - TEN_YEAR_DELTA
        if not is_range and value is not None:
            min_value = value - TEN_YEAR_DELTA
        elif is_range and len(value) != 0:
            min_value = value[0] - TEN_YEAR_DELTA

    if max_value is None:
        max_value = get_today() + TEN_YEAR_DELTA
        if not is_range and value is not None:
            max_value = value + TEN_YEAR_DELTA
        elif is_range and len(value) != 0:
            max_value = value[-1] + TEN_YEAR_DELTA
            
    return min_value, max_value

def _validate_date_values(url_key: str, value: Any, min_value: date, max_value: date, is_range: bool) -> None:
    """Validate that date values are within allowed range and correctly ordered."""
    if not is_range and value is not None:
        if value < min_value:
            raise ValueError(f"Selected date ({value}) is before the minimum allowed date ({min_value}).")
        if value > max_value:
            raise ValueError(f"Selected date ({value}) is after the maximum allowed date ({max_value}).")
    
    elif is_range and len(value) == 1:
        if value[0] < min_value:
            raise ValueError(f"Selected date ({value[0]}) is before the minimum allowed date ({min_value}).")
        if value[0] > max_value:
            raise ValueError(f"Selected date ({value[0]}) is after the maximum allowed date ({max_value}).")
    
    elif is_range and len(value) == 2:
        if value[0] > value[1]:
            raise ValueError(f"Invalid date range: start date ({value[0]}) is after end date ({value[1]}).")
        if value[0] < min_value:
            raise ValueError(f"Start date ({value[0]}) is before the minimum allowed date ({min_value}).")
        if value[1] > max_value:
            raise ValueError(f"End date ({value[1]}) is after the maximum allowed date ({max_value}).")

def handle_date_input(url_key: str, url_value: Optional[List[str]], bound_args: inspect.BoundArguments,
                    compressor: Callable, decompressor: Callable, **kwargs) -> Any:
    """
    Handle date input widget URL state synchronization.
    
    Manages bidirectional sync between date input widget state and URL parameters,
    supporting both single dates and date ranges. Handles validation of date formats,
    ranges, and boundary constraints.

    Args:
        url_key: URL parameter key for this date input
        url_value: Value(s) from URL, or None if not present
        bound_args: Bound arguments for the date input widget

    Returns:
        The date input widget's return value (date or tuple of dates)

    Raises:
        UrlParamError: If URL value is invalid
        ValueError: If date value is invalid
    """
    # Extract parameters from bound arguments
    min_date = bound_args.arguments.get('min_value', _DEFAULT_MIN_VALUE)
    max_date = bound_args.arguments.get('max_value', _DEFAULT_MAX_VALUE)
    value = bound_args.arguments.get('value', _DEFAULT_VALUE)

    # Parse and validate input values
    if isinstance(value, (list, tuple)):
        value = [_parse_date_input_value(v) for v in value]
    else:
        value = _parse_date_input_value(value)

    is_range = isinstance(value, (list, tuple))
    
    # Parse min/max values
    min_value = _parse_date_input_value(min_date)
    max_value = _parse_date_input_value(max_date)
    
    # Calculate default min/max values if not provided
    min_value, max_value = _calculate_min_max_dates(value, min_value, max_value, is_range)
    
    # Validate date values
    _validate_date_values(url_key, value, min_value, max_value, is_range)

    if url_value is None:
        init_url_value(url_key, compressor(to_url_value(value)))
        return st.date_input(**bound_args.arguments)
    
    url_value = decompressor(url_value)
        
    url_value = _parse_url_date_params(url_key, url_value, is_range)
    _check_date_bounds(url_key, url_value, min_value, max_value)
    bound_args.arguments['value'] = url_value
    
    return st.date_input(**bound_args.arguments)