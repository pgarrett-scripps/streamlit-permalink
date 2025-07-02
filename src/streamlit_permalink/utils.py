"""
Utility functions for streamlit_permalink.
"""

import base64
import warnings
import zlib
from datetime import date, datetime, time
from functools import partial
from typing import Any, Callable, Dict, Iterable, List, Optional, Tuple, Union
from urllib.parse import urlencode

import pandas as pd
import streamlit as st
from packaging.version import parse as V

from .constants import (
    DATAEDITOR_DATE_VALUE_PREFIX,
    DATAEDITOR_DATETIME_VALUE_PREFIX,
    DATAEDITOR_TIME_VALUE_PREFIX,
    EMPTY_LIST_URL_VALUE,
    EMPTY_STRING_URL_VALUE,
    NONE_URL_VALUE,
)


class TypedValue:
    """A class that converts a value to a string and makes it hashable."""

    def __init__(self, value: Any):
        self.value = value
        self.type: type = type(value)

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, "TypedValue"):
            return False
        return self.value == other.value and self.type == other.type

    def __hash__(self) -> int:
        return hash((str(self.value), self.type))

    def __repr__(self):
        return f"{self.value}({self.type.__name__})"


class StringHashableValue:
    """
    A class that converts a value to a string and makes it hashable.
    """

    def __init__(self, value: Any):
        self.value = value
        self.is_hashable = self._is_hashable(value)

    def _is_hashable(self, value: Any) -> bool:
        try:
            hash(value)
            return True
        except TypeError:
            return False

    def __eq__(self, other: Any) -> bool:
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


def serialize_df(df: pd.DataFrame) -> str:
    result = df.copy(deep=True)
    for col in df.columns:
        for idx in result.index:
            value = result.at[idx, col]  # type: ignore
            if isinstance(value, date) and not isinstance(value, datetime):
                result.at[idx, col] = f"{DATAEDITOR_DATE_VALUE_PREFIX}{value.isoformat()}"  # type: ignore
            elif isinstance(value, datetime):
                result.at[idx, col] = f"{DATAEDITOR_DATETIME_VALUE_PREFIX}{value.isoformat()}"  # type: ignore
            elif isinstance(value, time):
                result.at[idx, col] = f"{DATAEDITOR_TIME_VALUE_PREFIX}{value.strftime('%H:%M')}"  # type: ignore

    json_str: str = result.to_json(orient="records")  # type: ignore
    return json_str


def to_url_value(result: Any) -> Union[str, List[str]]:
    """
    Convert a result to a URL value.
    """
    if result is None:
        return NONE_URL_VALUE
    if isinstance(result, str):
        if result == "":
            return EMPTY_STRING_URL_VALUE
        return result
    if isinstance(result, (bool, float, int)):
        return str(result)
    if isinstance(result, (list, tuple)):
        if len(result) == 0:  # type: ignore
            return EMPTY_LIST_URL_VALUE
        return list(map(to_url_value, result))  # type: ignore
    if isinstance(result, (date, datetime)):
        return result.isoformat()
    if isinstance(result, time):
        return result.strftime("%H:%M")
    if isinstance(result, pd.DataFrame):
        return serialize_df(result)
    try:
        res = str(result)
        if res == "":
            return EMPTY_STRING_URL_VALUE
        return res
    except Exception as err:
        raise TypeError(f"unsupported type: {type(result)}") from err


def init_url_value(url_key: str, url_value: str):
    """Initialize a URL value."""

    if V(st.__version__) < V("1.30"):
        url = st.experimental_get_query_params()
        url[url_key] = [url_value]
        st.experimental_set_query_params(**url)
    else:
        st.query_params[url_key] = url_value


def validate_multi_options(
    options: Optional[Iterable[Any]], widget_name: str
) -> List[str]:
    """Validate multiselect options and convert to strings."""

    if options is None:
        raise ValueError(
            f"{widget_name.capitalize()} options cannot be None. Expected a non-empty list of options."
        )

    options = list(options)
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

    # provide warning when sets are different lengths
    if len(set(map(StringHashableValue, options))) != len(options):
        warnings.warn(
            f"Duplicate values detected in {widget_name} options: {options}. "
            "When these values are passed through URL parameters, the first matching value will be selected. "
            "This may lead to unexpected behavior if multiple options evaluate to the same string representation.",
            UserWarning,
        )

    return str_options


def validate_multi_default(
    default: Optional[Union[List[Any], Any]],
    options: Optional[Union[List[Any], Any]],
    widget_name: str,
) -> List[str]:
    """Validate multiselect default value and convert to list of strings."""

    if default is None:
        return []

    if not isinstance(default, Iterable):
        default = [default]

    if options is None:
        options = []

    # ensure that all default values are in the options list
    invalid_defaults = [v for v in default if v not in options]  # type: ignore
    if invalid_defaults:
        raise ValueError(
            f"Invalid default values for {widget_name}: {invalid_defaults}. "
            f"Valid options are: {options}"
        )

    return list(map(str, default))  # type: ignore


def validate_selection_mode(selection_mode: str) -> str:
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


def update_data_editor(df: pd.DataFrame, df_updates: Dict[str, Any]) -> pd.DataFrame:
    """Update a DataFrame based on the updates from the data editor."""

    for row_index, row_data in df_updates["edited_rows"].items():
        for column_name, value in row_data.items():
            df.at[int(row_index), column_name] = value  # type: ignore

    for row_data in df_updates["added_rows"]:
        df = pd.concat([df, pd.DataFrame([row_data])], ignore_index=True)

    for row_index in df_updates["deleted_rows"]:
        df = df.drop(row_index)

    return df


def to_list(value: Any) -> List[Any]:
    """Convert a value to a list if it's not already one."""

    if value is None:
        return []
    if isinstance(value, list):
        return value  # type: ignore
    return [value]


def get_query_params_url(params_dict: Dict[str, Any]) -> str:
    """
    Create URL query string from a dictionary of parameters.

    Args:
        params_dict (dict): A dictionary with parameter names as keys and values.

    Returns:
        str: A URL query string starting with '?'
    """
    # Convert nested params dict to flat list of tuples with repeated keys for multiple values
    query_items: List[Tuple[str, str]] = []
    for key, values in params_dict.items():
        values_list = to_list(values)
        for value in values_list:
            query_items.append((key, str(value)))

    # Use urlencode to properly handle URL encoding of parameters
    query_string = urlencode(query_items)
    return f"?{query_string}" if query_string else ""


def requires_streamlit_version(
    min_version: str,
) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
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

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            if V(st.__version__) < V(min_version):
                raise RuntimeError(
                    f"{func.__name__} requires Streamlit {min_version} or newer. "
                    f"Current version: {st.__version__}"
                )
            return func(*args, **kwargs)

        return wrapper

    return decorator


def get_query_params() -> Dict[str, List[str]]:
    """
    Get the current query parameters from the URL.

    Returns:
        dict: Dictionary of query parameters
    """

    if st.__version__ < "1.30":
        url_params = st.experimental_get_query_params()
    else:
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


def create_url(
    url: str,
    url_params: Optional[Dict[str, Any]] = None,
) -> str:
    """
    Create a URL with include the given values as query parameters.

    Args:
        url (str): Base URL
        url_params (dict): Dictionary of query parameters

    Returns:
        str: Complete URL with query parameters
    """
    if url_params is None:
        url_params = {}

    url_params = {k: to_url_value(v) for k, v in url_params.items()}

    # Handle URL with existing query parameters
    if "?" in url:
        base_url, existing_params = url.split("?", 1)
        return f"{base_url}{get_query_params_url(url_params)}&{existing_params}"

    return f"{url}{get_query_params_url(url_params)}"


def compress_list(func: Callable[..., str], l: Union[List[str], str]) -> List[str]:

    if l == EMPTY_LIST_URL_VALUE:
        return [EMPTY_LIST_URL_VALUE]

    if l == NONE_URL_VALUE:
        return [NONE_URL_VALUE]

    if l == EMPTY_STRING_URL_VALUE:
        return [EMPTY_STRING_URL_VALUE]

    if isinstance(l, str):
        return [func(l)]

    return [func(e) for e in l]


def decompress_list(func: Callable[..., Any], l: List[str]) -> Optional[List[Any]]:

    if l == [EMPTY_LIST_URL_VALUE]:
        return []

    if l == [NONE_URL_VALUE]:
        return None

    if l == [EMPTY_STRING_URL_VALUE]:
        return [""]

    l = [func(e) for e in l]

    return l


DEFAULT_COMPRESSOR = partial(compress_list, compress_text)
DEFAULT_DECOMPRESSOR = partial(decompress_list, decompress_text)
