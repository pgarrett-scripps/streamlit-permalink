"""
Handle slider widget URL state synchronization.
"""

from datetime import datetime, date, time, timedelta
from enum import Enum
from typing import Any, Callable, List, Optional, Union, Tuple
import inspect

import streamlit as st

from ..utils import init_url_value, to_url_value
from ..exceptions import UrlParamError

_HANDLER_NAME = "slider"


class SliderType(Enum):
    """Enumeration of supported slider types."""

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


def _get_defaults(
    min_value: Union[int, float, datetime, date, time, None],
    max_value: Union[int, float, datetime, date, time, None],
    value: Union[int, float, datetime, date, time, list, tuple, None],
    step: Union[int, float, timedelta, None],
) -> Tuple[Any, Any, Any, Any, SliderType]:
    """
    Verify and initialize slider parameters.

    Ensures min_value, max_value, value, and step are correct types and values,
    and initializes them with sensible defaults if needed.

    Returns:
        Tuple of (min_value, max_value, value, step, slider_type)
    """
    slider_type = _get_slider_type(min_value, max_value, value, step)

    # Handle min and value
    if min_value is not None and value is None:
        value = min_value
    elif value is not None and min_value is None:
        if isinstance(value, (list, tuple)):
            _value = value[0]
        else:
            _value = value
        if slider_type in (SliderType.SINGLE_DATE, SliderType.MULTI_DATE):
            min_value = _value - timedelta(days=14)
        elif slider_type in (SliderType.SINGLE_DATETIME, SliderType.MULTI_DATETIME):
            min_value = _value - timedelta(days=14)
        elif slider_type in (SliderType.SINGLE_TIME, SliderType.MULTI_TIME):
            min_value = time.min
        elif slider_type in (SliderType.SINGLE_INT, SliderType.MULTI_INT):
            min_value = min(_value, 0)
        elif slider_type in (SliderType.SINGLE_FLOAT, SliderType.MULTI_FLOAT):
            min_value = min(_value, 0.0)
        else:
            raise ValueError(f"Unsupported slider type: {slider_type}")
    elif min_value is None and value is None:
        min_value = 0
        value = 0

    # Handle max
    if max_value is None:
        if isinstance(value, (list, tuple)):
            _value = value[0]
        else:
            _value = value

        if slider_type in (SliderType.SINGLE_DATE, SliderType.MULTI_DATE):
            max_value = _value + timedelta(days=14)
        elif slider_type in (SliderType.SINGLE_DATETIME, SliderType.MULTI_DATETIME):
            max_value = _value + timedelta(days=14)
        elif slider_type in (SliderType.SINGLE_TIME, SliderType.MULTI_TIME):
            max_value = time.max
        elif slider_type in (SliderType.SINGLE_INT, SliderType.MULTI_INT):
            max_value = max(_value, 100)
        elif slider_type in (SliderType.SINGLE_FLOAT, SliderType.MULTI_FLOAT):
            max_value = max(_value, 1.0)
        else:
            raise ValueError(f"Unsupported slider type: {slider_type}")

    # Handle step
    if step is None:
        if slider_type in (SliderType.SINGLE_INT, SliderType.MULTI_INT):
            step = 1
        elif slider_type in (SliderType.SINGLE_FLOAT, SliderType.MULTI_FLOAT):
            step = 0.01
        elif slider_type in (SliderType.SINGLE_DATE, SliderType.MULTI_DATE):
            step = timedelta(days=1)
        elif slider_type in (SliderType.SINGLE_DATETIME, SliderType.MULTI_DATETIME):
            if max_value - min_value < timedelta(days=1):
                step = timedelta(minutes=15)
            else:
                step = timedelta(days=1)
        elif slider_type in (SliderType.SINGLE_TIME, SliderType.MULTI_TIME):
            step = timedelta(minutes=15)
        else:
            raise ValueError(f"Unsupported slider type: {slider_type}")

    return min_value, max_value, value, step, slider_type


def _validate_step(
    step: Union[int, float, timedelta, None], slider_type: SliderType
) -> None:
    """Validate that the step value is appropriate for the slider type."""
    if step is not None:
        if slider_type in (SliderType.SINGLE_INT, SliderType.MULTI_INT):
            if not isinstance(step, int):
                raise ValueError(
                    f"Step must be an integer for single or multi int slider: {step}"
                )
        if slider_type in (SliderType.SINGLE_FLOAT, SliderType.MULTI_FLOAT):
            if not isinstance(step, float):
                raise ValueError(
                    f"Step must be a float for single or multi float slider: {step}"
                )
        if slider_type in (
            SliderType.SINGLE_DATETIME,
            SliderType.MULTI_DATETIME,
            SliderType.SINGLE_DATE,
            SliderType.MULTI_DATE,
            SliderType.SINGLE_TIME,
            SliderType.MULTI_TIME,
        ):
            if not isinstance(step, timedelta):
                raise ValueError(
                    f"Step must be a timedelta for {slider_type.value} slider: {step}"
                )


def _get_slider_type(
    min_value: Union[int, float, datetime, date, time, None],
    max_value: Union[int, float, datetime, date, time, None],
    value: Union[int, float, datetime, date, time, None, list, tuple],
    step: Union[int, float, timedelta, None],
) -> SliderType:
    """
    Determine the slider type based on the provided parameters.

    Returns:
        SliderType: The determined slider type
    """
    option_types = {type(min_value), type(max_value)}
    if isinstance(value, (list, tuple)):
        if len(value) != 2:
            raise ValueError(
                f"Invalid value for slider parameter: {value}. Expected a list or tuple of length 2."
            )

        for v in value:
            option_types.add(type(v))
    else:
        option_types.add(type(value))

    # Remove None from option_types
    option_types = {t for t in option_types if t is not type(None)}

    if len(option_types) == 0:
        slider_type = SliderType.SINGLE_INT  # Default to single int
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
            else:
                raise ValueError(f"Unsupported slider type: {option_type}")
        else:
            if option_type == int:
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
        raise ValueError(
            f"All slider parameters must be of the same type: {option_types}"
        )

    _validate_step(step, slider_type)

    return slider_type


def handle_slider(
    base_widget: st.delta_generator.DeltaGenerator,
    url_key: str,
    url_value: Optional[List[str]],
    bound_args: inspect.BoundArguments,
    compressor: Callable,
    decompressor: Callable,
) -> Any:
    """
    Handle slider widget URL state synchronization.

    Args:
        base_widget: The base widget to handle
        url_key: Parameter key in URL
        url_value: Value(s) from URL parameter, None if not present
        bound_args: Bound arguments for the base_widget call
        compressor: Compressor function for url_value
        decompressor: Decompressor function for url_value

    Returns:
        The slider widget's return value

    Raises:
        UrlParamError: If URL values are invalid, out of bounds, or of wrong type
    """
    # Get slider parameters
    min_value = bound_args.arguments.get("min_value")
    max_value = bound_args.arguments.get("max_value")
    value = bound_args.arguments.get("value")
    step = bound_args.arguments.get("step")

    min_value, max_value, value, step, slider_type = _get_defaults(
        min_value, max_value, value, step
    )

    # If no URL value, set it to the default value
    if not url_value:
        init_url_value(url_key, compressor(to_url_value(value)))
        return base_widget(**bound_args.arguments)

    url_value = decompressor(url_value)

    # Determine if this is a range slider based on the initial value
    is_multi = isinstance(value, (list, tuple))
    expected_values = 2 if is_multi else 1

    # Validate number of values matches slider type
    if len(url_value) != expected_values:
        raise UrlParamError(
            f"Invalid number of values for {_HANDLER_NAME} parameter '{url_key}': got {len(url_value)}, "
            f"expected {expected_values} ({'range' if is_multi else 'single'} slider)"
        )

    try:
        # Parse values based on type
        if slider_type in (SliderType.SINGLE_INT, SliderType.MULTI_INT):
            parsed_values = [int(v) for v in url_value]
        elif slider_type in (SliderType.SINGLE_FLOAT, SliderType.MULTI_FLOAT):
            parsed_values = [float(v) for v in url_value]
        elif slider_type in (SliderType.SINGLE_DATE, SliderType.MULTI_DATE):
            parsed_values = [datetime.strptime(v, "%Y-%m-%d").date() for v in url_value]
        elif slider_type in (SliderType.SINGLE_DATETIME, SliderType.MULTI_DATETIME):
            parsed_values = [
                datetime.strptime(v, "%Y-%m-%dT%H:%M:%S") for v in url_value
            ]
        elif slider_type in (SliderType.SINGLE_TIME, SliderType.MULTI_TIME):
            parsed_values = [datetime.strptime(v, "%H:%M").time() for v in url_value]
        else:
            raise ValueError(f"Unsupported slider type: {slider_type}")
    except ValueError as err:
        raise UrlParamError(
            f"Invalid value(s) for {_HANDLER_NAME} parameter '{url_key}': {url_value}. "
            f"Expected {slider_type.name} value(s). Error: {str(err)}"
        ) from err

    # Validate parsed values
    if is_multi:
        if len(parsed_values) != 2:
            raise UrlParamError(
                f"Invalid number of values for {_HANDLER_NAME} parameter '{url_key}': {len(parsed_values)}. "
                "Expected 2 values for range slider."
            )

        if parsed_values[0] > parsed_values[1]:
            raise UrlParamError(
                f"Invalid range for {_HANDLER_NAME} parameter '{url_key}': "
                f"start value {parsed_values[0]} is greater than end value {parsed_values[1]}."
            )

        # Check that parsed values are within bounds
        if parsed_values[0] < min_value or parsed_values[1] > max_value:
            raise UrlParamError(
                f"Invalid range for {_HANDLER_NAME} parameter '{url_key}': "
                f"range values {parsed_values} are outside bounds [{min_value}, {max_value}]."
            )

        bound_args.arguments["value"] = tuple(parsed_values)
    else:
        if len(parsed_values) != 1:
            raise UrlParamError(
                f"Invalid number of values for {_HANDLER_NAME} parameter '{url_key}': {len(parsed_values)}. "
                "Expected 1 value for single slider."
            )

        # Check that parsed value is within bounds
        if parsed_values[0] < min_value or parsed_values[0] > max_value:
            raise UrlParamError(
                f"Invalid value for {_HANDLER_NAME} parameter '{url_key}': "
                f"value {parsed_values[0]} is outside bounds [{min_value}, {max_value}]."
            )

        bound_args.arguments["value"] = parsed_values[0]

    return base_widget(**bound_args.arguments)
