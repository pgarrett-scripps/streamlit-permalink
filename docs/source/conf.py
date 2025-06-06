"""
Configuration file for the Sphinx documentation builder.
"""

import os
import sys
import datetime

# Add the project root directory to the path
sys.path.insert(0, os.path.abspath('../..'))

# Mock imports for modules we can't install on ReadTheDocs
autodoc_mock_imports = ["streamlit", "pandas"]

# Import project information
import streamlit_permalink

# -- Project information -----------------------------------------------------
project = 'streamlit-permalink'
copyright = f'{datetime.datetime.now().year}, Patrick Garrett'
author = 'Patrick Garrett'
version = streamlit_permalink.__version__
release = streamlit_permalink.__version__

# -- General configuration ---------------------------------------------------
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
    'sphinx.ext.napoleon',
    'sphinx.ext.intersphinx',
    'sphinx.ext.coverage',
    'sphinx.ext.todo',
    'sphinx.ext.autosummary',
    'sphinx_autodoc_typehints',
    'sphinx.ext.githubpages',
    'autoapi.extension',
]

# Napoleon settings
napoleon_google_docstring = False
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = True
napoleon_include_private_with_doc = False
napoleon_include_special_with_doc = True
napoleon_use_admonition_for_examples = False
napoleon_use_admonition_for_notes = False
napoleon_use_admonition_for_references = False
napoleon_use_ivar = False
napoleon_use_param = True
napoleon_use_rtype = True
napoleon_preprocess_types = False
napoleon_type_aliases = None
napoleon_attr_annotations = True

# AutoAPI settings
autoapi_type = 'python'
autoapi_dirs = ['../../streamlit_permalink']
autoapi_add_toctree_entry = True
autoapi_python_class_content = 'both'
autoapi_member_order = 'groupwise'
autoapi_options = ['members', 'undoc-members', 'show-inheritance', 'show-module-summary']

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
exclude_patterns = []

# -- Options for HTML output -------------------------------------------------
html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
html_logo = None
html_favicon = None

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

# Intersphinx mapping
intersphinx_mapping = {
    'python': ('https://docs.python.org/3', None),
}

# -- Options for todo extension ----------------------------------------------
todo_include_todos = True
