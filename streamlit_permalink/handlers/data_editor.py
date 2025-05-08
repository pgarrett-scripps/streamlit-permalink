from typing import Any, Optional
from io import StringIO

import streamlit as st
import pandas as pd

from .handler import HandleWidget


def fix_datetime_columns(
    df: pd.DataFrame, column_config: Optional[dict]
) -> pd.DataFrame:
    """
    Fix datetime columns in a DataFrame based on column configuration.
    """
    if not column_config:
        return df

    for column_name, config in column_config.items():
        col_type = config["type_config"]["type"]
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


class HandlerDataEditor(HandleWidget):

    def __init__(self, *args, **kwargs):
        """
        Initialize the HandlerPills instance.
        """
        super().__init__(*args, **kwargs)

        # Add column_config to to session state, sinec it is not part of the data
        st.session_state[
            f"STREAMLIT_PERMALINK_DATA_EDITOR_COLUMN_CONFIG_{self.url_key}"
        ] = self.bound_args.arguments.get("column_config")

    # Override the url_init method to set the initial fromt he data rather than return
    def url_init(self, widget_value: Any) -> None:
        """
        Initialize the URL value(s) in the query params.
        """
        st.session_state[f"STREAMLIT_PERMALINK_DATA_EDITOR_{self.url_key}"] = (
            self.bound_args.arguments.get("data")
        )
        if self.init_url:
            self.update_url_param(self.bound_args.arguments.get("data"))

    def update_bound_args(self) -> None:

        # Process URL value: ensure single value and convert to boolean
        parsed_value = self.validate_single_url_value(self.url_value, allow_none=False)
        df = pd.read_json(StringIO(parsed_value), orient="records")
        df = fix_datetime_columns(df, self.bound_args.arguments.get("column_config"))
        st.session_state[f"STREAMLIT_PERMALINK_DATA_EDITOR_{self.url_key}"] = df
        self.bound_args.arguments["data"] = df
