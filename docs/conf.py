
project = "ldfparser"
copyright = "Balazs Eszes, 2023"
author = "Balazs Eszes"

release = "0.20.0"

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.extlinks",
    "sphinx.ext.autosectionlabel"
]

template_path = ['_templates']

autosectionlabel_prefix_document = True
autosectionlabel_maxdepth = 2

autoclass_content = "init"

html_theme = 'sphinx_rtd_theme'

html_static_path = ['_static']
html_extra_path = ['.nojekyll']

_repo = ''

extlinks = {
    "pypi": ("project/%s", "%s")
}
