Streamlit Permalink Documentation
================================

.. image:: https://readthedocs.org/projects/streamlit-permalink/badge/?version=latest
   :target: https://streamlit-permalink.readthedocs.io/en/latest/?badge=latest
   :alt: Documentation Status

Effortless permalinks in Streamlit apps. Synchronize Streamlit widgets with URL query params.

Quick Start
-----------

Replace regular Streamlit widgets with URL-aware versions:

.. code-block:: python

   import streamlit as st
   import streamlit_permalink as stp

   # Regular widget
   name = st.text_input("Your name")

   # URL-aware widget - state saved in URL
   name = stp.text_input("Your name", url_key="name")

Contents
--------

.. toctree::
   :maxdepth: 2

   installation
   usage
