# Effortless permalinks in Streamlit apps

This is my fork of streamlit-permalink: https://github.com/franekp/streamlit-permalink. 

### Installation

```bash
pip install streamlit-permalink-pg
```

### Basic usage

The `streamlit_permalink` (shorthand: stp) namespace contains url-aware versions of almost all input widgets from Streamlit. General usage of input widgets is described in [Streamlit docs](https://docs.streamlit.io/library/api-reference/widgets). 

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

### Examples

Several example applications demonstrating various use cases are available:

1. Browse the [examples folder](examples/) in the repository
2. Try the interactive documentation app:
  - Locally: `streamlit run examples/docs_app.py`
  - Online: Visit [permalink.streamlit.app](https://permalink.streamlit.app)


### Note regarding `url_Key`
A `url_key` is required for all widgets. If not specified:
1. The widget's `key` value will be used as `url_key`
2. If no `key` is present, the widget's label will be used

When `url_key` is specified, it also sets the widget's `key`. Therefore, it's recommended to use only `url_key`:

```python
import streamlit_permalink as stp

# Using key parameter makes the widget URL-aware
text1 = stp.text_input('Type some text', url_key='secret')
# If the user typed 'foobar' into the above text field, the
# URL would end with '?secret=foobar' at this point.
```

### Usage inside forms

To use URL-aware widgets inside Streamlit forms, you need to use `st.form` and `st.form_submit_button`, which are the URL-aware counterparts of Streamlit's form functions:

```python
import streamlit_permalink as stp
import streamlit as st

with stp.form('some-form'):
  text = stp.text_input('Text field inside form', url_key='secret')
  # At this point the URL query string is empty / unchanged, even
  # if the user has edited the text field.
  if stp.form_submit_button('Submit'):
    # URL is updated only when users hit the submit button
    st.write(text)
```

Or with alternative syntax:

```python
import streamlit_permalink as stp

form = stp.form('some-form')
form.text_input('Text field inside form', url_key='secret')
# At this point the URL query string is empty / unchanged, even
# if the user has edited the text field.
if form.form_submit_button('Submit'):
  # URL is updated only when users hit the submit button
  st.write(text)
```

### Compression

For widgets that may contain large amounts of text (like `text_area`), you can enable compression to reduce the URL length. 

```python
import streamlit_permalink as stp

# Enable compression for text area content
long_text = stp.text_area("Enter long text", url_key="essay", compress=True)
# The text will be compressed before being added to the URL
```

By default, compression uses a built-in text compression algorithm. You can also provide custom compression and decompression functions:

```python
import streamlit_permalink as stp
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
long_text = stp.text_area(
    "Enter long text", 
    url_key="essay", 
    compress=True,
    compressor=custom_compress,
    decompressor=custom_decompress
)
```

Compression also works with lists, such as in `multiselect` widgets, where each item in the list will be compressed individually.

### Disabling URL-aware Statefulness

In some cases, you might want to use a widget without URL-aware functionality. You can disable this by setting `stateful=False`:

```python
import streamlit_permalink as stp

# This widget will behave like a regular Streamlit widget
# and won't update the URL or be controlled by URL parameters
text = stp.text_input("Enter text", url_key="non_url_text", stateful=False)
```

This is useful when you have widgets that should not affect the shareable state of your application.

### Configuring URL Value Initialization

By default all stp widgets will automatically populate thier url value upon initialization. This can be turned off by passing init_url=False to the stp widget.

```python
import streamlit_permalink as stp

text = stp.text_input("Enter text", url_key="text_input", init_url=False)
```

### Setting URL Values

Methods to set the URL value are available for each widget using set_url_value. URL value validation is minimal, since the actual widgets args are not accessible. Ensure that any value set by set_url_value is valid for the widget you are setting it for.

```python
import streamlit_permalink as stp

# basic
stp.checkbox.set_url_value(value=True, url_key='checkbox1')

# compression
stp.checkbox.set_url_value(value=True, url_key='checkbox2', compress=True)

# custom compression
stp.checkbox.set_url_value(value=True, url_key='checkbox3', compress=True, compressor=CUSTOM_COMPRESSION_FUNC)
```

### Getting URL Values

likewise use, get_url_value to retrive the url value for widgets. Again, since the actual widget args are not available only minimal validation can be done. multiselect, pills, and segmented_control will return str values regardless of what options are provided.

```python
import streamlit_permalink as stp

# basic
stp.checkbox.get_url_value(url_key='checkbox1')

# compression
stp.checkbox.get_url_value(url_key='checkbox2', compress=True)

# custom compression
stp.checkbox.get_url_value(url_key='checkbox3', compress=True, decompressor=CUSTOM_DECOMPRESSION_FUNC)

```

### Development and Testing

To set up the development environment and run tests:

1. Clone the repository and install in editable mode with test dependencies:
```bash
git clone https://github.com/pgarrett-scripps/streamlit-permalink
cd streamlit-permalink
pip install -e ".[test]"
```

2. Run the tests:
```bash
# Run all tests
pytest tests

# Run a specific test file
pytest tests/test_checkbox.py
```
