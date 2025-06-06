Installation
============

Install via pip:

.. code-block:: bash

   pip install streamlit-permalink-pg

That's it! Now you can import and use URL-aware widgets:

.. code-block:: python

   import streamlit_permalink as stp

   # Use any widget with url_key parameter
   name = stp.text_input("Your name", url_key="name")
