import os

# setup documentation metadata

project = 'SyNAP'
copyright = '2024, Synaptics'
author = 'Synaptics'
release = os.environ.get('RELEASE_VER', 'git-main')

# setup html theme

html_static_path = ['_static']

exclude_patterns = ["README.rst"]

extensions = [
    'sphinx_rtd_theme',
    'sphinxcontrib.plantuml',
    'breathe',
    'myst_parser',
]

myst_enable_extensions = [
    "html_admonition",
]

html_theme = "sphinx_rtd_theme"

templates_path = [ '_templates' ]

html_context = {
    'display_github': True,
    'github_repo': 'synaptics-synap/doc',
    'github_version': 'main',
    'conf_py_path': '/',
    'version': release,
}

# setup inclusion of doxygen documentation extracted from sources

breathe_projects = {
    'runtime': '_build/doxygen/xml'
}

breathe_default_project = 'runtime'

# this code is used to substitute #xx# variables anywhere in the source, even
# inside literal blocks and code blocks

def preprocess_variables(app, docname, source):
    for varname, value in app.config.preprocessor_variables.items():
        source[0] = source[0].replace(varname, value)


preprocessor_variables = {
    "#release#": release
}


def setup(app):

    # add support for pre-processing
    app.add_config_value('preprocessor_variables', {}, True)
    app.connect('source-read', preprocess_variables)

    # add custom theme overrides and javascript
    app.add_css_file('css/synaptics.css')
    app.add_js_file('js/synaptics.js')
