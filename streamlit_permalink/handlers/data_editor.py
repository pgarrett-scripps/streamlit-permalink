"""
Handle dataeditor widget URL state synchronization.
"""

from io import StringIO
from typing import Callable, List, Optional
import inspect

import streamlit as st
import pandas as pd

from ..utils import (
    fix_datetime_columns,
    init_url_value,
    to_url_value,
    validate_single_url_value,
)

_HANDLER_NAME = "data_editor"


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
    st.session_state[f"STREAMLIT_PERMALINK_DATA_EDITOR_COLUMN_CONFIG_{url_key}"] = (
        bound_args.arguments.get("column_config")
    )

    # Initialize from default when no URL value exists
    if url_value is None:
        #  SAVE ORIGINAL DF
        st.session_state[f"STREAMLIT_PERMALINK_DATA_EDITOR_{url_key}"] = (
            bound_args.arguments.get("data")
        )
        init_url_value(
            url_key, compressor(to_url_value(bound_args.arguments.get("data")))
        )
        return base_widget(**bound_args.arguments)

    url_value = decompressor(url_value)  # [str, str], [], None

    # Process URL value: ensure single value and convert to boolean
    validated_value = validate_single_url_value(url_key, url_value, _HANDLER_NAME)
    df = pd.read_json(StringIO(validated_value), orient="records")
    df = fix_datetime_columns(df, bound_args.arguments.get("column_config"))
    st.session_state[f"STREAMLIT_PERMALINK_DATA_EDITOR_{url_key}"] = df

    bound_args.arguments["data"] = df
    return base_widget(**bound_args.arguments)
