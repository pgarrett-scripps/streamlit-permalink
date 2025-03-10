# Effortless permalinks in Streamlit apps

### Installation

```bash
pip install streamlit-permalink
```

### Basic usage

The `streamlit_permalink` (shorthand: `stp`) namespace contains url-aware versions of almost all input widgets from Streamlit:

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
* `stp.feedback`
* `stp.segmented_control`

In addition to standard input widgets, it also has an url-aware version of the [streamlit-option-menu](https://github.com/victoryhb/streamlit-option-menu) component: `stp.option_menu`. For this to work, `streamlit-option-menu` must be installed separately.

General usage of input widgets is described in [Streamlit docs](https://docs.streamlit.io/library/api-reference/widgets). Url-aware widgets additionally take one more keyword argument: `url_key`. It is the name of the query parameter in the URL under which the widget's state will be persisted:

```python
import streamlit_permalink as stp

text = stp.text_input('Type some text', url_key='secret')
# If the user typed 'foobar' into the above text field, the
# URL would end with '?secret=foobar' at this point.
```

Once widget state is saved into the URL, it can be shared and whoever opens the URL will see the same widget state as the person that has shared it.

\
Widget state will be url-persisted only if `url_key` is present, otherwise `stp.<widget-name>` behaves exactly the same as `st.<widget-name>`:

```python
import streamlit_permalink as stp

text = stp.text_input('Type some text')
# URL query string will be empty at this point,
# no matter whether the above text field is empty or not
```

By default, the value of `url_key` is also used as the `key` parameter of the Streamlit widget: 

```python
import streamlit as st
import streamlit_permalink as stp

text = stp.text_input('Type some text', url_key='secret')
st.write(st.session_state.secret)
```

However, it is possible to provide different values of `url_key` and `key`:

```python
import streamlit as st
import streamlit_permalink as stp

text = stp.text_input('Type some text', url_key='secret', key='different_name')
st.write(st.session_state.different_name)
```

### Usage inside forms

To use URL-aware widgets inside Streamlit forms, you need to use `stp.form` and `stp.form_submit_button`, which are the URL-aware counterparts of `st.form` and `st.form_submit_button`:

```python
import streamlit_permalink as stp

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

\

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

The test suite includes comprehensive tests for all supported Streamlit widgets, covering both standalone and form-based usage scenarios.
