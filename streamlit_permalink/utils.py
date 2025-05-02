"""
Utility functions for streamlit_permalink.
"""

import base64
from datetime import date, datetime, time
import re
from typing import Any, Iterable, List, Optional, Union
import zlib
import warnings
from urllib.parse import quote_plus
from packaging.version import parse as V

import pandas as pd
import streamlit as st

from .constants import _EMPTY, _NONE, TRUE_VALUE, TRUE_FALSE_VALUE
from .exceptions import UrlParamError


class TypedValue:
    """
    A class that converts a value to a string and makes it hashable.
    """

    def __init__(self, value):
        self.value = value
        self.type = type(value)

    def __eq__(self, other):
        if not isinstance(other, TypedValue):
            return False
        return self.value == other.value and self.type == other.type

    def __hash__(self):
        return hash((str(self.value), self.type))

    def __repr__(self):
        return f"{self.value}({self.type.__name__})"


class StringHashableValue:
    """
    A class that converts a value to a string and makes it hashable.
    """

    def __init__(self, value):
        self.value = value
        self.is_hashable = self._is_hashable(value)

    def _is_hashable(self, value):
        try:
            hash(value)
            return True
        except TypeError:
            return False

    def __eq__(self, other):
        if not isinstance(other, StringHashableValue):
            return False
        if self.is_hashable and other.is_hashable:
            return self.value == other.value
        return str(self.value) == str(other.value)

    def __hash__(self):
        if self.is_hashable:
            return hash(self.value)
        return hash(str(self.value))

    def __repr__(self):
        return f"{self.value}"


def to_url_value(result: Any) -> Union[str, List[str]]:
    """
    Convert a result to a URL value.
    """
    if result is None:
        return _NONE
    if isinstance(result, str):
        return result
    if isinstance(result, (bool, float, int)):
        return str(result)
    if isinstance(result, (list, tuple)):
        if len(result) == 0:
            return _EMPTY
        return list(map(to_url_value, result))
    if isinstance(result, (date, datetime)):
        return result.isoformat()
    if isinstance(result, time):
        return result.strftime("%H:%M")
    if isinstance(result, pd.DataFrame):
        # return as json string
        return result.to_json(orient="records")
    try:
        return str(result)
    except Exception as err:
        raise TypeError(f"unsupported type: {type(result)}") from err


def init_url_value(url_key: str, url_value: str):
    """
    Initialize a URL value.
    """
    if V(st.__version__) < V("1.30"):
        url = st.experimental_get_query_params()
        url[url_key] = url_value
        st.experimental_set_query_params(**url)
    else:
        st.query_params[url_key] = url_value


def parse_time(time_str: str) -> time:
    """
    Parse a time string into a time object.
    """
    return datetime.strptime(time_str, "%H:%M").time()


def validate_single_url_value(
    url_key: str, url_value: Optional[List[str]], handler_name: str
) -> Optional[str]:
    """
    Validate single value from URL parameter.
    """
    if url_value is None:
        return None

    if not (isinstance(url_value, (list, tuple)) and len(url_value) == 1):
        raise UrlParamError(
            f"Invalid value for {handler_name} parameter '{url_key}': {url_value}. Expected a single value."
        )

    return url_value[0]


def validate_bool_url_value(url_key: str, url_value: str, handler_name: str) -> bool:
    """
    Validate boolean value from URL parameter.
    """
    url_value = url_value.capitalize()  # Case insensitive
    if url_value not in TRUE_FALSE_VALUE:
        raise UrlParamError(
            f"Invalid value for {handler_name} parameter '{url_key}': {url_value}. Expected a {TRUE_FALSE_VALUE}."
        )
    return url_value == TRUE_VALUE


def validate_color_url_value(url_key: str, url_value: str, handler_name: str) -> str:
    """
    Validate color value from URL parameter.
    """
    if not re.match(r"^#([0-9a-fA-F]{6})$", url_value):
        raise UrlParamError(
            f"Invalid value for {handler_name} parameter '{url_key}': {url_value}. "
            "Expected a valid hex color code (e.g., #RRGGBB)."
        )
    return url_value


def validate_date_url_value(url_key: str, url_value: str, handler_name: str) -> str:
    """
    Validate date value from URL parameter.
    """
    try:
        return datetime.strptime(url_value, "%Y-%m-%d").date()
    except ValueError as err:
        raise UrlParamError(
            f"Invalid value for {handler_name} parameter '{url_key}': {url_value}. "
            "Expected a valid date (e.g., 2023-01-01)."
        ) from err


def _validate_multi_options(options: Iterable[Any], widget_name: str) -> List[str]:
    """
    Validate multiselect options and convert to strings.
    """
    if options is None:
        raise ValueError(
            f"{widget_name.capitalize()} options cannot be None. Expected a non-empty list of options."
        )

    if not isinstance(options, Iterable):
        raise ValueError(
            f"Invalid value for {widget_name} options: {options}. Expected an iterable."
        )

    if len(options) == 0:
        raise ValueError(
            f"{widget_name.capitalize()} options cannot be empty. Expected a non-empty list of options."
        )

    str_options = list(map(str, options))

    # must use typed value since options like 1 and True will be equal
    unique_options = set(TypedValue(o) for o in options)
    unique_str_options = set(TypedValue(o) for o in str_options)

    if len(unique_options) != len(unique_str_options):
        raise ValueError(
            f"{widget_name.capitalize()} options must be unique when cast to strings. "
            f"Options: {options}, "
            f"String options: {str_options}"
        )

    # provide warning is normla sets are different lengths
    if len(set(map(StringHashableValue, options))) != len(options):
        warnings.warn(
            f"Duplicate values detected in {widget_name} options: {options}. "
            "When these values are passed through URL parameters, the first matching value will be selected. "
            "This may lead to unexpected behavior if multiple options evaluate to the same string representation.",
            UserWarning,
        )

    return str_options


def _validate_multi_default(
    default: Union[List[Any], Any, None],
    options: Union[List[Any], Any, None],
    widget_name: str,
) -> List[str]:
    """
    Validate multiselect default value and convert to list of strings.
    """
    if default is None:
        return []

    if not isinstance(default, Iterable):
        default = [default]

    # ensure that all default values are in the options list
    invalid_defaults = [v for v in default if v not in options]
    if invalid_defaults:
        raise ValueError(
            f"Invalid default values for {widget_name}: {invalid_defaults}. "
            f"Valid options are: {options}"
        )

    return list(map(str, default))


def _validate_multi_url_values(
    url_key: str,
    url_values: Optional[List[str]],
    str_options: List[str],
    widget_name: str,
) -> List[str]:
    """
    Validate that all multiselect values are in the options list.
    """
    # Handle special case for empty selection
    if url_values is None:
        return []

    # Validate all values are in options
    invalid_values = [v for v in url_values if v not in str_options]
    if invalid_values:
        raise UrlParamError(
            f"Invalid {widget_name.capitalize()} selection for '{url_key}': {invalid_values}. "
            f"Valid options are: {str_options}"
        )

    return url_values


def _validate_selection_mode(selection_mode: str) -> str:
    """
    Validate selection mode and convert to string.
    """
    if selection_mode not in ("single", "multi"):
        raise ValueError(
            f"Invalid selection_mode: {selection_mode}. Expected 'single' or 'multi'."
        )
    return selection_mode


def compress_text(text: str) -> str:
    """
    Compress text using zlib and encode with base64 to make it URL-compatible.

    Args:
        text: The text to compress

    Returns:
        URL-compatible compressed string
    """
    compressed = zlib.compress(
        text.encode("utf-8"), level=9
    )  # Level 0-9, 9 is highest compression
    encoded = base64.urlsafe_b64encode(compressed).decode("utf-8")
    return encoded


def decompress_text(compressed_text: str) -> str:
    """
    Decompress text that was compressed with compress_text.

    Args:
        compressed_text: The compressed text

    Returns:
        Original decompressed text
    """
    decoded = base64.urlsafe_b64decode(compressed_text)
    decompressed = zlib.decompress(decoded).decode("utf-8")
    return decompressed


def fix_datetime_columns(
    df: pd.DataFrame, column_config: Optional[dict]
) -> pd.DataFrame:
    """
    Fix datetime columns in a DataFrame based on column configuration.
    """
    if not column_config:
        return df

    for column_name, column_config in column_config.items():
        col_type = column_config["type_config"]["type"]
        if col_type == "datetime":
            # Convert milliseconds from epoch to datetime
            df[column_name] = pd.to_datetime(df[column_name], unit="ms")
        elif col_type == "date":
            # Convert milliseconds from epoch to date
            df[column_name] = pd.to_datetime(df[column_name], unit="ms").dt.date
        elif col_type == "time":
            # For time values that are already strings in HH:MM:SS format
            if df[column_name].dtype == "object":
                df[column_name] = pd.to_datetime(
                    df[column_name], format="%H:%M:%S"
                ).dt.time
            else:
                # For time values stored as milliseconds since midnight
                df[column_name] = pd.to_datetime(df[column_name], unit="ms").dt.time

    return df


def update_data_editor(df: pd.DataFrame, df_updates: dict) -> pd.DataFrame:
    """
    Update a DataFrame based on the updates from the data editor.
    """

    for row_index, row_data in df_updates["edited_rows"].items():
        for column_name, value in row_data.items():
            df.at[int(row_index), column_name] = value

    for row_data in df_updates["added_rows"]:
        df = pd.concat([df, pd.DataFrame([row_data])], ignore_index=True)

    for row_index in df_updates["deleted_rows"]:
        df = df.drop(row_index)

    return df


def to_list(value: Any) -> List:
    """Convert a value to a list if it's not already one."""
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]


def get_query_params_url(params_dict: dict) -> str:
    """
    Create URL query string from a dictionary of parameters.

    Args:
        params_dict (dict): A dictionary with parameter names as keys and values.

    Returns:
        str: A URL query string starting with '?'
    """
    params = []
    for key, values in params_dict.items():
        for value in to_list(values):
            params.append(f"{key}={quote_plus(str(value))}")

    return "?" + "&".join(params)


def requires_streamlit_version(min_version: str):
    """
    Decorator to check if the current Streamlit version meets the minimum requirement.

    Args:
        min_version (str): Minimum required Streamlit version

    Returns:
        function: Wrapped function that checks version before execution

    Example:
        @requires_streamlit_version("1.45.0")
        def my_function():
            # Function implementation
    """

    def decorator(func):
        def wrapper(*args, **kwargs):
            if V(st.__version__) < V(min_version):
                raise RuntimeError(
                    f"{func.__name__} requires Streamlit {min_version} or newer. "
                    f"Current version: {st.__version__}"
                )
            return func(*args, **kwargs)

        return wrapper

    return decorator


def get_query_params() -> dict[str, List]:
    """
    Get the current query parameters from the URL.

    Returns:
        dict: Dictionary of query parameters
    """

    if st.__version__ < "1.30":
        url_params = {
            k: st.experimental_get_query_params[k]
            for k in st.experimental_get_query_params.keys()
        }

    url_params = {k: st.query_params.get_all(k) for k in st.query_params.keys()}
    return url_params


@requires_streamlit_version("1.45.0")
def get_page_url() -> str:
    """
    Get the current page URL including query parameters.

    Returns:
        str: Complete URL with query parameters
    """
    url_params = get_query_params()
    return f"{st.context.url}{get_query_params_url(url_params)}"
