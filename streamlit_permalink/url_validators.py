import re
from typing import List, Optional

from .constants import FALSE_URL_VALUE, TRUE_URL_VALUE


def is_valid_color(value: str) -> bool:
    """
    Check if the given value is a valid color in the format #RRGGBB.
    """
    return bool(re.match(r"^#([0-9a-fA-F]{6})$", value))


def validate_color(value: str) -> str:
    """
    Validate that the value is a valid color.
    """
    if not is_valid_color(value):
        raise ValueError(f"Invalid color format: {value}. Expected format: #RRGGBB.")
    return value


def validate_bool(value: str) -> bool:
    """
    Validate that the value is a boolean.
    """
    value = value.capitalize()
    if value not in [TRUE_URL_VALUE, FALSE_URL_VALUE]:
        raise ValueError(
            f"Invalid value for checkbox: '{value}'. Expected {TRUE_URL_VALUE} or {FALSE_URL_VALUE}."
        )

    return value == TRUE_URL_VALUE


def validate_single_url_value(
    url_value: Optional[List[str]] = None,
    allow_none: bool = False,
) -> Optional[str]:
    """
    Validate single value from URL parameter.
    """
    if url_value is None:

        if not allow_none:
            raise ValueError("None value is not allowed.")

        return None

    if not (isinstance(url_value, (list, tuple)) and len(url_value) == 1):
        raise ValueError("Expected a single value, but got multiple values.")

    return url_value[0]


def validate_multi_url_values(
    url_values: Optional[List[str]] = None,
    min_values: Optional[int] = None,
    max_values: Optional[int] = None,
    allow_none: bool = False,
) -> List[str]:
    """
    Validate that all multiselect values are in the options list.
    """
    # Handle special case for empty selection
    if url_values is None:

        if not allow_none:
            raise ValueError("None value is not allowed.")

        return []

    if not isinstance(url_values, (list, tuple)):
        raise ValueError("Expected a list of values.")

    if min_values is not None and len(url_values) < min_values:
        raise ValueError(
            f"Expected at least {min_values} values, but got {len(url_values)}."
        )

    if max_values is not None and len(url_values) > max_values:
        raise ValueError(
            f"Expected at most {max_values} values, but got {len(url_values)}."
        )

    return url_values
