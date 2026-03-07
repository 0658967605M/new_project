import os
import sys

sys.path.insert(0, os.path.abspath('../..'))  # path to Django project

# -- Project information -----------------------------------------------------

project = 'new_project'
copyright = '2026, en'
author = 'en'
release = 'today'

# -- General configuration ---------------------------------------------------

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
]

templates_path = ['_templates']
exclude_patterns = []

# -- Options for HTML output -------------------------------------------------

html_theme = 'alabaster'
html_static_path = ['_static']
