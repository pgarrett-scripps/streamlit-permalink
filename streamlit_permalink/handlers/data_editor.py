"""
Handle dataeditor widget URL state synchronization.
"""

import base64
from io import StringIO
import json
import pickle
from typing import Callable, List, Optional
import inspect
import ast

import streamlit as st
import pandas as pd

from ..utils import (
    init_url_value,
    to_url_value,
    validate_single_url_value,
)

_HANDLER_NAME = "data_editor"
_DEFAULT_DATA = pd.DataFrame()




def handle_data_editor(
    base_widget: st.delta_generator.DeltaGenerator,
    url_key: str,
    url_value: Optional[List[str]],
    bound_args: inspect.BoundArguments,
    compressor: Callable,
    decompressor: Callable,
) -> bool:
    """
    Handle data_editor widget URL state synchronization.
    """

    # TODO: URL VALIDATION FOR COLUM CONFIGS

    # Initialize from default when no URL value exists
    if url_value is None:
        #  SAVE ORIGINAL DF
        st.session_state[f'STREAMLIT_PERMALINK_DATA_EDITOR_{url_key}'] = bound_args.arguments.get("data")
        init_url_value(url_key, compressor(to_url_value(bound_args.arguments.get("data"))))
        return base_widget(**bound_args.arguments)

    url_value = decompressor(url_value)  # [str, str], [], None

    # Process URL value: ensure single value and convert to boolean
    validated_value = validate_single_url_value(url_key, url_value, _HANDLER_NAME)

    # get df from json string
    df = pd.read_json(StringIO(validated_value), orient='records')

    column_config = bound_args.arguments.get("column_config")

    if column_config is not None:
        for column_name, column_config in column_config.items():
            print(f'column_name: {column_name}, column_config: {column_config["type_config"]["type"]}')
            print(df[column_name])
            col_type = column_config['type_config']['type']
            if col_type == 'datetime':
                # Convert milliseconds from epoch to datetime
                df[column_name] = pd.to_datetime(df[column_name], unit='ms')
            elif col_type == 'date':
                # Convert milliseconds from epoch to date
                df[column_name] = pd.to_datetime(df[column_name], unit='ms').dt.date
            elif col_type == 'time':
                # For time values that are already strings in HH:MM:SS format
                if df[column_name].dtype == 'object':
                    df[column_name] = pd.to_datetime(df[column_name], format='%H:%M:%S').dt.time
                else:
                    # For time values stored as milliseconds since midnight
                    df[column_name] = pd.to_datetime(df[column_name], unit='ms').dt.time



    bound_args.arguments["data"] = df

    st.session_state[f'STREAMLIT_PERMALINK_DATA_EDITOR_{url_key}'] = df

    return base_widget(**bound_args.arguments)

