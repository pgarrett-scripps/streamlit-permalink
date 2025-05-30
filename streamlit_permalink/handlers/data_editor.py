from ..constants import DATAEDITOR_COLUMN_CONFIG_PREFIX, DATAEDITOR_DATE_VALUE_PREFIX, DATAEDITOR_DATETIME_VALUE_PREFIX, DATAEDITOR_PREFIX, DATAEDITOR_TIME_VALUE_PREFIX
from ..url_validators import validate_single_url_value
from .handler import WidgetHandler
from typing import Any
from io import StringIO

import streamlit as st
import pandas as pd

from .handler import WidgetHandler

# TODO: Update df to prefix STREAMLIT_PERMALINK_TIME in front of time values ratehr than requiring col config


def fix_datetime_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Fix datetime columns in a DataFrame based on column configuration.
    """
    df = df.copy(deep=True)

    for col in df.columns:
        for idx in df.index:
            value = df.at[idx, col]
            if isinstance(value, str):
                if value.startswith(DATAEDITOR_DATE_VALUE_PREFIX):
                    df.at[idx, col] = pd.to_datetime(
                        value.replace(DATAEDITOR_DATE_VALUE_PREFIX, "")
                    ).date()
                elif value.startswith(DATAEDITOR_DATETIME_VALUE_PREFIX):
                    df.at[idx, col] = pd.to_datetime(
                        value.replace(DATAEDITOR_DATETIME_VALUE_PREFIX, "")
                    )
                elif value.startswith(DATAEDITOR_TIME_VALUE_PREFIX):
                    df.at[idx, col] = pd.to_datetime(
                        value.replace(DATAEDITOR_TIME_VALUE_PREFIX, ""), format="%H:%M"
                    ).time()

    return df


class DataEditorHandler(WidgetHandler):

    def __init__(self, *args, **kwargs):
        """
        Initialize the HandlerPills instance.
        """
        super().__init__(*args, **kwargs)

        # Add column_config to to session state, sinec it is not part of the data
        st.session_state[
            f"{DATAEDITOR_COLUMN_CONFIG_PREFIX}{self.url_key}"
        ] = self.bound_args.arguments.get("column_config")

    # Override the url_init method to set the initial fromt he data rather than return
    def url_init(self, widget_value: Any) -> None:
        """
        Initialize the URL value(s) in the query params.
        """
        st.session_state[f"{DATAEDITOR_PREFIX}{self.url_key}"] = (
            self.bound_args.arguments.get("data")
        )
        if self.init_url:
            self.update_url_param(self.bound_args.arguments.get("data"))

    def sync_query_params(self) -> None:

        # Process URL value: ensure single value and convert to boolean
        parsed_value = self.validate_single_url_value(self.url_value, allow_none=False)
        df = pd.read_json(StringIO(parsed_value), orient="records")
        df = fix_datetime_columns(df)
        st.session_state[f"{DATAEDITOR_PREFIX}{self.url_key}"] = df
        self.bound_args.arguments["data"] = df

    @classmethod
    def verify_update_url_value(cls, value: Any) -> Any:
        if not isinstance(value, pd.DataFrame):
            raise ValueError(
                f"Data value must be a pandas DataFrame, got {type(value)}"
            )
        return value

    @classmethod
    def verify_get_url_value(cls, value: Any) -> Any:
        parsed_value = validate_single_url_value(value, allow_none=False)
        df = pd.read_json(StringIO(parsed_value), orient="records")
        return [df]
