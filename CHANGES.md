# 1.5.1 Release Notes
- bug fix for get_url_value - some widgets didnt returna a list

# 1.5.0 Release Notes
- Added class methods for getting and setting url values to each WidgetHandler
    - available under stp.widget.get_url_value and stp.widget.set_url_value
- Fixed DataEditor syncing issue with date, datetime, and time values

# 1.4.0 Release Notes
- Fixed Naming
- URL Building functions (to_url_value & create_url)
- STP constants available from namespace

# 1.3.0 Release Notes

## Changes
- Added support for `accept_new_options` to multiselect and selectbox (for streamlit v1.45)
- Added functions: `get_query_params` and `get_page_url` (for streamlit v1.45)
- Revert docs & examples to use `url_key` for widget creation.
- Added support for `stp.data_editor`
- Added handler base class, and refactored handlers to use this
- Url value init now optional
- Added "_STREAMLIT_PERMALINK_EMPTY_STRING" to the possible stp query values. 
- Compression will no longer compress _STREAMLIT_PERMALINK_* values
- Created docs_app.py (interractive documentation)

# 1.2.0 Release Notes

## Changes
- Improved code organization
- Added comprehensive type annotations
- Added support for `pills` and `segmented_control` widgets
- Added test suite for all supported widgets (except `pills` and `segmented_control` as their testing functions are not yet available)
- Implemented GitHub Actions CI/CD pipeline with tests running across multiple Python versions (3.9-3.12)
- Fixed multi-date input handling and setting date to None
- Widgets now preserve original types instead of casting everything to strings
- Automatic URL value generation on first widget initialization
- Widgets which support multiple states (slider, pills, etc.) can no longer be switched by editing query parameters
- Now uses Python's `inspect` module to ensure proper argument mapping
- Made `url_key` parameter optional when `key` is provided (if `url_key` is provided, it will be used for both)
- Added optional URL compression (useful for very long text_areas) by passing `compress=True` to widgets
- Added support for custom compression/encoding of URL values by passing appropriate functions to `compressor` and `decompressor` parameters
- Statefulness can be disabled by passing `stateful=False`

## Future Roadmap
- Add test coverage for `pills`, `segmented_control` & `data_editor` widgets once testing functions become available
- Remove support for `st.option_menu`?
- Add `data_editor` url value validation

