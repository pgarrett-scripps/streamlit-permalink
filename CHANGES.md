# 1.1.0 Release Notes

## Changes
- Added support for `stp.data_editor`

# 1.0.1 Release Notes

## Changes
- Bug fix for widget url compression in forms


# 1.0.0 Release Notes

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
- Add test coverage for `pills` and `segmented_control` widgets once testing functions become available
- Refactor and enhance test cases for improved reliability and maintainability
- Implement configurable initialization of default values, with special consideration for form components
- Evaluate the necessity of both `_EMPTY` and `_NONE` constants, ensuring consistent usage across all widgets
- Consider adding optional synchronization of additional parameters (e.g., `max_chars`, `options`) with URL state

