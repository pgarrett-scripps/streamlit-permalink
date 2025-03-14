# Streamlit Permalink 1.0.0 Release Notes

## Changes
- Improved code organization with better separation of concerns
- Added comprehensive type annotations with Python 3.8-3.12 compatibility
- Added support for `pills` and `segmented_control` widgets
- Added comprehensive test suite for all supported widgets (except `pills` and `segmented_control` since their testing functions are not yet available)
- Implemented Github Actions CI/CD pipeline with tests running across multiple Python versions (3.9-3.12)
- Fixed multi-date input handling
- Enhanced widget behavior to preserve original types instead of casting everything to strings
- Implemented automatic URL value generation on first widget initialization
- Improved widget consistency: widgets supporting multi/single inputs can no longer be switched by editing query parameters
- Now uses Python's `inspect` module to ensure proper argument mapping
- Made `url_key` parameter optional when `key` is provided (if `url_key` is provided, it will be used for both)

## Future Roadmap
- Add test coverage for `pills` and `segmented_control` widgets once testing functions become available
- Refactor and enhance test cases for improved reliability and maintainability
- Implement configurable initialization of default values, with special consideration for form components
- Evaluate the necessity of both `_EMPTY` and `_NONE` constants, ensuring consistent usage across all widgets
- Add optional synchronization of additional parameters (e.g., `max_chars`, `options`) with URL state

