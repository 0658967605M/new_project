import os
import sys
import django

# Add Django project path
sys.path.insert(0, os.path.abspath('../..'))

# Set Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'new_project.settings')

# Setup Django
django.setup()

# -- Project information -----------------------------------------------------

project = 'new_project'
author = 'Manqoba Hlongwane'
release = '1.0'

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
