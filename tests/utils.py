import streamlit as st
from packaging.version import parse as V

def get_query_params(app_test):
    """Helper function to get query parameters that works with both old and new Streamlit versions"""
    if V(st.__version__) < V('1.30'):
        return app_test.experimental_get_query_params()
    return app_test.query_params

def set_query_params(app_test, params):
    """Helper function to set query parameters that works with both old and new Streamlit versions"""
    if V(st.__version__) < V('1.30'):
        app_test.experimental_set_query_params(**params)
    else:
        app_test.query_params.update(params)