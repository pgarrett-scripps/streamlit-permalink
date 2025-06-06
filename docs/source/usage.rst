Usage
=====

Getting Started
--------------

Replace Streamlit widgets with their URL-aware versions from ``streamlit_permalink`` (``stp``):

.. code-block:: python

   import streamlit as st
   import streamlit_permalink as stp

   # Regular Streamlit widget
   name = st.text_input("Your name")

   # URL-aware version - saves state in URL
   name = stp.text_input("Your name", url_key="name")

Every widget needs a ``url_key`` to identify it in the URL. When you change the widget value, the URL updates automatically.

Forms Support
------------

To use URL-aware widgets inside Streamlit forms, you need to use ``stp.form`` and ``stp.form_submit_button``, which are the URL-aware counterparts of Streamlit's form functions:

.. code-block:: python

   import streamlit_permalink as stp
   import streamlit as st

   with stp.form('some-form'):
     text = stp.text_input('Text field inside form', url_key='secret')
     # At this point the URL query string is empty / unchanged, even
     # if the user has edited the text field.
     if stp.form_submit_button('Submit'):
       # URL is updated only when users hit the submit button
       st.write(text)

Or with alternative syntax:

.. code-block:: python

   import streamlit_permalink as stp

   form = stp.form('some-form')
   form.text_input('Text field inside form', url_key='secret')
   # At this point the URL query string is empty / unchanged, even
   # if the user has edited the text field.
   if form.form_submit_button('Submit'):
     # URL is updated only when users hit the submit button
     st.write(text)

Compression/Decompression of URL values
------------------

For widgets that may contain large amounts of text (like ``text_area``), you can enable compression to reduce the URL length:

.. code-block:: python

   import streamlit_permalink as stp

   # Enable compression for text area content
   long_text = stp.text_area("Enter long text", url_key="essay", compress=True)
   # The text will be compressed before being added to the URL

By default, compression uses a built-in text compression algorithm. You can also provide custom compression and decompression functions:

.. code-block:: python

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

Compression also works with lists, such as in ``multiselect`` widgets, where each item in the list will be compressed individually.

Disabling URL-aware Statefulness
-------------------------------

In some cases, you might want to use a widget without URL-aware functionality. You can disable this by setting ``stateful=False``:

.. code-block:: python

   import streamlit_permalink as stp

   # This widget will behave like a regular Streamlit widget
   # and won't update the URL or be controlled by URL parameters
   text = stp.text_input("Enter text", url_key="non_url_text", stateful=False)

This is useful when you have widgets that should not affect the shareable state of your application.

Configuring URL Value Initialization
----------------------------------

By default, all stp widgets will automatically populate their URL value upon initialization. This can be turned off by passing ``init_url=False`` to the stp widget:

.. code-block:: python

   import streamlit_permalink as stp

   text = stp.text_input("Enter text", url_key="text_input", init_url=False)

Setting URL Values
---------------------------------

Methods to set the URL value are available for each widget using ``set_url_value``. URL value validation is minimal since the actual widgets args are not accessible. Ensure that any value set by ``set_url_value`` is valid for the widget you are setting it for:

.. code-block:: python

   import streamlit_permalink as stp

   # basic
   stp.checkbox.set_url_value(value=True, url_key='checkbox1')

   # compression
   stp.checkbox.set_url_value(value=True, url_key='checkbox2', compress=True)

   # custom compression
   stp.checkbox.set_url_value(value=True, url_key='checkbox3', compress=True, compressor=CUSTOM_COMPRESSION_FUNC)

Getting URL Values
---------------------------------

Likewise, use ``get_url_value`` to retrieve the URL value for widgets. Again, since the actual widget args are not available, only minimal validation can be done. ``multiselect``, ``pills``, and ``segmented_control`` will return string values regardless of what options are provided:

.. code-block:: python

   import streamlit_permalink as stp

   # basic
   stp.checkbox.get_url_value(url_key='checkbox1')

   # compression
   stp.checkbox.get_url_value(url_key='checkbox2', compress=True)

   # custom compression
   stp.checkbox.get_url_value(url_key='checkbox3', compress=True, decompressor=CUSTOM_DECOMPRESSION_FUNC)

Available Widgets
----------------

* ``stp.checkbox``
* ``stp.radio``
* ``stp.selectbox``
* ``stp.multiselect``
* ``stp.slider``
* ``stp.select_slider``
* ``stp.text_input``
* ``stp.number_input``
* ``stp.text_area``
* ``stp.date_input``
* ``stp.time_input``
* ``stp.color_picker``
* ``stp.form_submit_button``
* ``stp.pills``
* ``stp.segmented_control``
* ``stp.toggle``
* ``stp.data_editor``

In addition to standard input widgets, it also has an URL-aware version of the `streamlit-option-menu <https://github.com/victoryhb/streamlit-option-menu>`_ component: ``st.option_menu``. For this to work, ``streamlit-option-menu`` must be installed separately.


Avoid Using st.stop() with Streamlit-Permalink
--------------------

Using ``st.stop()`` in your Streamlit apps can cause desynchronization issues with URL parameters. 
When ``st.stop()`` is called, it can sometimes cause widgets to desynch from their url values.

**Problem:**

.. code-block:: python

   import streamlit as st
   import streamlit_permalink as stp
   
   user_input = stp.text_input("Enter something", url_key="input")
   
   if not user_input:
       st.warning("Please enter a value")
       st.stop()  # This can cause URL sync issues!
   
   # The code below may not execute, preventing URL sync
   st.write(f"You entered: {user_input}")

**Recommended approach:**

Instead of using ``st.stop()``, use conditional statements to control the flow of your application:

.. code-block:: python

   import streamlit as st
   import streamlit_permalink as stp
   
   user_input = stp.text_input("Enter something", url_key="input")
   
   if not user_input:
       st.warning("Please enter a value")
   else:
       st.write(f"You entered: {user_input}")