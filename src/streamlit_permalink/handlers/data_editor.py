"""Handler for the st.data_editor widget."""

from io import StringIO
from typing import Any

import pandas as pd
import streamlit as st

from ..constants import (
    DATAEDITOR_COLUMN_CONFIG_PREFIX,
    DATAEDITOR_DATE_VALUE_PREFIX,
    DATAEDITOR_DATETIME_VALUE_PREFIX,
    DATAEDITOR_PREFIX,
    DATAEDITOR_TIME_VALUE_PREFIX,
)
from ..url_validators import validate_single_url_value_disallow_none
from .handler import WidgetHandler

# TODO: Update df to prefix STREAMLIT_PERMALINK_TIME in front of time values ratehr than requiring col config


def fix_datetime_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Fix datetime columns in a DataFrame based on column configuration."""

    df = df.copy(deep=True)

    for col in df.columns:
        for idx in df.index:
            value = df.at[idx, col]  # type: ignore
            if isinstance(value, str):
                if value.startswith(DATAEDITOR_DATE_VALUE_PREFIX):
                    df.at[idx, col] = pd.to_datetime(  # type: ignore
                        value.replace(DATAEDITOR_DATE_VALUE_PREFIX, "")
                    ).date()
                elif value.startswith(DATAEDITOR_DATETIME_VALUE_PREFIX):
                    df.at[idx, col] = pd.to_datetime(  # type: ignore
                        value.replace(DATAEDITOR_DATETIME_VALUE_PREFIX, "")
                    )
                elif value.startswith(DATAEDITOR_TIME_VALUE_PREFIX):
                    df.at[idx, col] = pd.to_datetime(  # type: ignore
                        value.replace(DATAEDITOR_TIME_VALUE_PREFIX, ""), format="%H:%M"
                    ).time()

    return df


class DataEditorHandler(WidgetHandler):
    """Handler for the st.data_editor widget."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Initialize the HandlerPills instance."""

        super().__init__(*args, **kwargs)

        # Add column_config to to session state, sinec it is not part of the data
        st.session_state[f"{DATAEDITOR_COLUMN_CONFIG_PREFIX}{self.url_key}"] = (
            self.bound_args.arguments.get("column_config")
        )

    # Override the url_init method to set the initial from the data rather than return
    def url_init(self, widget_value: Any) -> None:  # type: ignore
        """Initialize the URL value(s) in the query params."""

        st.session_state[f"{DATAEDITOR_PREFIX}{self.url_key}"] = (
            self.bound_args.arguments.get("data")
        )
        if self.init_url:
            self.update_url_param(self.bound_args.arguments.get("data"))

    def sync_query_params(self) -> None:
        """Sync data editor value with URL parameter."""

        parsed_value = self.validate_single_url_value_disallow_none(self.url_value)
        df = pd.read_json(StringIO(parsed_value), orient="records")  # type: ignore
        df = fix_datetime_columns(df)
        st.session_state[f"{DATAEDITOR_PREFIX}{self.url_key}"] = df
        self.bound_args.arguments["data"] = df

    @classmethod
    def verify_update_url_value(cls, value: Any) -> Any:
        """Verify that the value is a pandas DataFrame."""

        if not isinstance(value, pd.DataFrame):
            raise ValueError(
                f"Data value must be a pandas DataFrame, got {type(value)}"
            )
        return value

    @classmethod
    def verify_get_url_value(cls, value: Any) -> Any:
        """Get the URL value from the data editor."""

        parsed_value = validate_single_url_value_disallow_none(value)
        df = pd.read_json(StringIO(parsed_value), orient="records")  # type: ignore
        return [df]
