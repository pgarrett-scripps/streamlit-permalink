# Effortless permalinks in Streamlit apps

### Installation

```bash
pip install streamlit-permalink
```

### Basic usage

The `streamlit_permalink` (shorthand: stp) namespace contains url-aware versions of almost all input widgets from Streamlit:

* `stp.checkbox`
* `stp.radio`
* `stp.selectbox`
* `stp.multiselect`
* `stp.slider`
* `stp.select_slider`
* `stp.text_input`
* `stp.number_input`
* `stp.text_area`
* `stp.date_input`
* `stp.time_input`
* `stp.color_picker`
* `stp.form_submit_button`
* `stp.pills`
* `stp.segmented_control`
* `stp.toggle`
* `stp.data_editor`

In addition to standard input widgets, it also has an url-aware version of the [streamlit-option-menu](https://github.com/victoryhb/streamlit-option-menu) component: `st.option_menu`. For this to work, `streamlit-option-menu` must be installed separately.

General usage of input widgets is described in [Streamlit docs](https://docs.streamlit.io/library/api-reference/widgets). streamlit_permalink widgets require a `key` to be provided. 

```python
import streamlit_permalink as stp

# Using key parameter makes the widget URL-aware
text1 = stp.text_input('Type some text', key='secret')
# If the user typed 'foobar' into the above text field, the
# URL would end with '?secret=foobar' at this point.
```

Once widget state is saved into the URL, it can be shared and whoever opens the URL will see the same widget state as the person that has shared it.

### Note about Data Editor

- Date, Datetime, and Time columns must be declared using the column configs or the values will be converted to the number of ms since epoch.

### Usage inside forms

To use URL-aware widgets inside Streamlit forms, you need to use `st.form` and `st.form_submit_button`, which are the URL-aware counterparts of Streamlit's form functions:

```python
import streamlit_permalink as stp
import streamlit as st

with stp.form('some-form'):
  text = stp.text_input('Text field inside form', key='secret')
  # At this point the URL query string is empty / unchanged, even
  # if the user has edited the text field.
  if stp.form_submit_button('Submit'):
    # URL is updated only when users hit the submit button
    st.write(text)
```

Or with alternative syntax:

```python
import streamlit_permalink as st

form = st.form('some-form')
form.text_input('Text field inside form', key='secret')
# At this point the URL query string is empty / unchanged, even
# if the user has edited the text field.
if form.form_submit_button('Submit'):
  # URL is updated only when users hit the submit button
  st.write(text)
```

### Compression

For widgets that may contain large amounts of text (like `text_area`), you can enable compression to reduce the URL length. 

```python
import streamlit_permalink as st

# Enable compression for text area content
long_text = st.text_area("Enter long text", key="essay", compress=True)
# The text will be compressed before being added to the URL
```

By default, compression uses a built-in text compression algorithm. You can also provide custom compression and decompression functions:

```python
import streamlit_permalink as st
import gzip
import base64

def custom_compress(value: str) -> str:
    # Compress the string and encode the binary result as base64
    compressed = gzip.compress(value.encode('utf-8'))
    return base64.b64encode(compressed).decode('utf-8')

def custom_decompress(value: str) -> str:
    # Decode the base64 string back to binary and then decompress
    binary_data = base64.b64decode(value.encode('utf-8'))
    return gzip.decompress(binary_data).decode('utf-8')

# Use custom compression for a text area
long_text = st.text_area(
    "Enter long text", 
    key="essay", 
    compress=True,
    compressor=custom_compress,
    decompressor=custom_decompress
)
```

Compression also works with lists, such as in `multiselect` widgets, where each item in the list will be compressed individually.

### Disabling URL-aware Statefulness

In some cases, you might want to use a widget without URL-aware functionality. You can disable this by setting `stateful=False`:

```python
import streamlit_permalink as st

# This widget will behave like a regular Streamlit widget
# and won't update the URL or be controlled by URL parameters
text = st.text_input("Enter text", key="non_url_text", stateful=False)
```

This is useful when you have widgets that should not affect the shareable state of your application.

### Development and Testing

To set up the development environment and run tests:

1. Clone the repository and install in editable mode with test dependencies:
```bash
git clone https://github.com/franekp/streamlit-permalink.git
cd streamlit-permalink
pip install -e ".[test]"
```

2. Run the tests:
```bash
# Run all tests
pytest

# Run a specific test file
pytest tests/test_checkbox.py
```
