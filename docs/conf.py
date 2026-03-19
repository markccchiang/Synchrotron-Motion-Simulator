# Configuration file for the Sphinx documentation builder.

project = 'Synchrotron Motion Simulator'
copyright = '2014, Cheng-Chin Chiang'
author = 'Cheng-Chin Chiang'
release = '1.0'

extensions = [
    'sphinx.ext.mathjax',
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

html_theme = 'alabaster'
html_static_path = ['_static']
