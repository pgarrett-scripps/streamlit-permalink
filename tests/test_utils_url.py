"""Tests for URL-related utility functions in streamlit_permalink."""

import pytest
from streamlit_permalink.utils import create_url


def test_create_url_basic():
    """Test creating a URL with basic parameters."""
    url = "https://example.com"
    params = {"param1": "value1", "param2": "value2"}
    result = create_url(url, params)
    assert result == "https://example.com?param1=value1&param2=value2"


def test_create_url_no_params():
    """Test creating a URL without any parameters."""
    url = "https://example.com"
    result = create_url(url)
    assert result == "https://example.com"


def test_create_url_with_existing_params():
    """Test creating a URL that already has query parameters."""
    url = "https://example.com?existing=value"
    params = {"param1": "value1", "param2": "value2"}
    result = create_url(url, params)
    assert result == "https://example.com?param1=value1&param2=value2&existing=value"


def test_create_url_with_special_chars():
    """Test creating a URL with parameters containing special characters."""
    url = "https://example.com"
    params = {"param": "hello world", "other": "a+b=c"}
    result = create_url(url, params)
    assert result == "https://example.com?param=hello+world&other=a%2Bb%3Dc"


def test_create_url_with_none_value():
    """Test creating a URL with None value in parameters."""
    url = "https://example.com"
    params = {"param": None}
    result = create_url(url, params)
    assert result == "https://example.com?param=_STREAMLIT_PERMALINK_NONE"


def test_create_url_with_bool_values():
    """Test creating a URL with boolean values in parameters."""
    url = "https://example.com"
    params = {"true_param": True, "false_param": False}
    result = create_url(url, params)
    assert result == "https://example.com?true_param=True&false_param=False"


def test_create_url_with_list_values():
    """Test creating a URL with list values in parameters."""
    url = "https://example.com"
    params = {"list_param": [1, 2, 3]}
    result = create_url(url, params)
    assert result == "https://example.com?list_param=1&list_param=2&list_param=3"


def test_create_url_with_empty_list():
    """Test creating a URL with an empty list parameter."""
    url = "https://example.com"
    params = {"empty_list": []}
    result = create_url(url, params)
    assert result == "https://example.com?empty_list=_STREAMLIT_PERMALINK_EMPTY"
