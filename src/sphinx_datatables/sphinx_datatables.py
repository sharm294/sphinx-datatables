# Copyright (c) 2023 Varun Sharma
#
# SPDX-License-Identifier: MIT

"""Main file for the package."""

import importlib.metadata
from pathlib import Path
from typing import Any

import packaging.version
from docutils import nodes
from sphinx.application import Sphinx
from sphinx.errors import ExtensionError

from .config import SphinxDatatablesConfig
from .directives import add_directives
from .js import create_datatables_js


def add_datatables_scripts(
    app: Sphinx,
    _pagename: str,
    _templatename: str,
    _context: dict,
    _doctree: nodes.document,
) -> None:
    """Add the scripts to enable Datatables."""
    config = SphinxDatatablesConfig.from_sphinx_config(app.config)

    # Set up jQuery first, to verify it is available and gracefully output an error
    try:
        app.setup_extension("sphinxcontrib.jquery")
    except ExtensionError:  # pragma: no cover
        msg = (
            "sphinxcontrib.jquery is required for sphinx-datatables to work."
            " Please add it to your extensions in conf.py."
        )
        raise ExtensionError(msg) from None

    datetables_version_str = config.datatables_version
    if packaging.version.parse(datetables_version_str) < packaging.version.parse(
        "2.0.0",
    ):
        datatables_js = f"https://cdn.datatables.net/{datetables_version_str}/js/jquery.dataTables.min.js"
        datatables_css = f"https://cdn.datatables.net/{datetables_version_str}/css/jquery.dataTables.min.css"
    else:
        # for DataTables 2.0.0 and above, only the minified version is available
        # and jQuery is not included
        datatables_js = f"https://cdn.datatables.net/v/dt/dt-{datetables_version_str}/datatables.min.js"
        datatables_css = f"https://cdn.datatables.net/v/dt/dt-{datetables_version_str}/datatables.min.css"

    if config.datatables_js:
        datatables_js = config.datatables_js

    if config.datatables_css:
        datatables_css = config.datatables_css

    app.add_js_file(datatables_js)
    app.add_css_file(datatables_css)
    app.add_js_file("activate_datatables.js")


def finish(app: Sphinx, _exception: Exception | None) -> None:
    """
    Save the assets to the static directory.

    This function is called as the build finishes.

    Args:
        app (Sphinx): Sphinx app
        _exception (Exception | None): Any exceptions from the build

    """
    config = SphinxDatatablesConfig.from_sphinx_config(app.config)
    datatables_config_contents = create_datatables_js(config)
    asset_file = Path(app.builder.outdir) / "_static/activate_datatables.js"
    with asset_file.open("w+") as f:
        f.write(datatables_config_contents)


def setup(app: Sphinx) -> dict[str, Any]:
    """
    Set up the extension.

    Args:
        app (Sphinx): Sphinx app

    """
    app.add_config_value("datatables_version", "2.3.5", "html", str)
    app.add_config_value("datatables_class", "sphinx-datatable", "html", str)
    app.add_config_value("datatables_options", {}, "html", [dict, str])
    app.add_config_value("datatables_js", "", "html", str)
    app.add_config_value("datatables_css", "", "html", str)

    add_directives(app)

    app.connect("html-page-context", add_datatables_scripts)
    app.connect("build-finished", finish)

    return {
        "version": importlib.metadata.version("sphinx_datatables"),
        "env_version": None,  # unset := no cache versioning required by this extension
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
