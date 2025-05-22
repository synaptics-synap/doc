project = 'SyNAP'
copyright = '2024, Synaptics'
author = 'Synaptics'
release = '3.1.0'

extensions = [ 'synaptics_sphinx_theme' ]

# setup inclusion of doxygen documentation extracted from sources
breathe_projects = {
    'runtime': '_build/doxygen/xml'
}

html_theme_options = { 
    'logo_only': False
}

breathe_default_project = 'runtime'
