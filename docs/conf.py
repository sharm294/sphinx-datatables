# Copyright (c) 2023 Varun Sharma
#
# SPDX-License-Identifier: MIT

"""Sphinx configuration."""

# -- Project information -----------------------------------------------------

project = "sphinx-datatables"
copyright = "2023 Varun Sharma"  # noqa: A001
author = "Varun Sharma"

# override this value to build different versions
version = "master"

release = f"v{version}" if version != "master" else version

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

html_last_updated_fmt = "%B %d, %Y"
