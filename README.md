# Effortless permalinks in Streamlit apps

### Installation

```bash
pip install streamlit-permalink
```

### Basic usage

The `streamlit_permalink` namespace contains url-aware versions of almost all input widgets from Streamlit:

* `st.checkbox`
* `st.radio`
* `st.selectbox`
* `st.multiselect`
* `st.slider`
* `st.select_slider`
* `st.text_input`
* `st.number_input`
* `st.text_area`
* `st.date_input`
* `st.time_input`
* `st.color_picker`
* `st.form_submit_button`
* `st.pills`
* `st.segmented_control`
* `st.toggle`

In addition to standard input widgets, it also has an url-aware version of the [streamlit-option-menu](https://github.com/victoryhb/streamlit-option-menu) component: `st.option_menu`. For this to work, `streamlit-option-menu` must be installed separately.

The `streamlit_permalink` namespace now includes all Streamlit functions, so you can completely replace `import streamlit as st` with `import streamlit_permalink as st` in your code.

General usage of input widgets is described in [Streamlit docs](https://docs.streamlit.io/library/api-reference/widgets). streamlit_permalink widgets require a `key` to be provided:

```python
import streamlit_permalink as st

# Using key parameter makes the widget URL-aware
text1 = st.text_input('Type some text', key='secret')
# If the user typed 'foobar' into the above text field, the
# URL would end with '?secret=foobar' at this point.
```

Once widget state is saved into the URL, it can be shared and whoever opens the URL will see the same widget state as the person that has shared it.

### Usage inside forms

To use URL-aware widgets inside Streamlit forms, you need to use `st.form` and `st.form_submit_button`, which are the URL-aware counterparts of Streamlit's form functions:

```python
import streamlit_permalink as st

with st.form('some-form'):
  text = st.text_input('Text field inside form', key='secret')
  # At this point the URL query string is empty / unchanged, even
  # if the user has edited the text field.
  if st.form_submit_button('Submit'):
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
