# Configuration file for the Sphinx documentation builder.

project = 'Synchrotron Motion Simulator'
copyright = '2014, Cheng-Chin Chiang'
author = 'Cheng-Chin Chiang'
release = '0.1'

extensions = [
    'sphinx.ext.mathjax',
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

html_theme = 'alabaster'
html_static_path = ['_static']

# Project mark, shared with the README (assets/ lives outside the docs tree).
html_logo = '../assets/logo.svg'
html_favicon = '../assets/logo.svg'
html_theme_options = {
    'logo_name': True,
}
