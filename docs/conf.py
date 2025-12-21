# Copyright (c) 2023 Varun Sharma
#
# SPDX-License-Identifier: MIT

# -- Project information -----------------------------------------------------

project = "sphinx-datatables"
copyright = "2023 Varun Sharma"
author = "Varun Sharma"

# override this value to build different versions
version = "master"

if version != "master":
    release = f"v{version}"
else:
    release = version

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinxcontrib.jquery",
    # adds .nojekyll to the generated HTML for GitHub
    "sphinx.ext.githubpages",
    "sphinx.ext.napoleon",
    "sphinx_datatables",
    "sphinx_toolbox.collapse",
    "sphinx_copybutton",
]

# raise a warning if a cross-reference cannot be found
nitpicky = True

# Configure 'Edit on GitHub' extension
edit_on_github_project = "sharm294/sphinx-datatables"
edit_on_github_branch = f"{release}/docs"

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = [
    "_build",
    "Thumbs.db",
    ".DS_Store",
]

# -- Options for HTML output -------------------------------------------------

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
# html_static_path = ["_static"]

html_last_updated_fmt = "%B %d, %Y"

# -- Options for DataTables

datatables_selector_options = {
    "table.sphinx-datatable-20-30-50": {
        "columnDefs": [
            {"width": "20%", "targets": 0},
            {"width": "30%", "targets": 1},
            {"width": "50%", "targets": 2},
        ]
    }
}
