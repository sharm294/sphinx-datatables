# Copyright (c) 2023 Varun Sharma
#
# SPDX-License-Identifier: MIT

"""Main file for the package."""

import importlib.metadata
import json
import textwrap
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import packaging.version
from docutils import nodes
from sphinx.application import Sphinx
from sphinx.errors import ExtensionError

INDENT = " " * 4


@dataclass
class Config:
    """Holds the configuration data for the extension."""

    datatables_version: str
    datatables_class: str
    datatables_options: dict | str
    datatables_js: str
    datatables_css: str


def get_config(app: Sphinx) -> Config:
    """
    Return the configurable options.

    Args:
        app (Sphinx): Sphinx app

    Returns:
        Config: Dataclass for the config options

    """
    return Config(
        datatables_version=app.config.datatables_version,
        datatables_class=app.config.datatables_class,
        datatables_options=app.config.datatables_options,
        datatables_js=app.config.datatables_js,
        datatables_css=app.config.datatables_css,
    )


def add_datatables_scripts(
    app: Sphinx,
    _pagename: str,
    _templatename: str,
    _context: dict,
    _doctree: nodes.document,
) -> None:
    """Add the scripts to enable Datatables."""
    config = get_config(app)

    # Set up jQuery first, to verify it is available and gracefully output an error
    try:
        app.setup_extension("sphinxcontrib.jquery")
    except ExtensionError:
        msg = (
            "sphinxcontrib.jquery is required for sphinx-datatables to work.",
            "Please add it to your extensions in conf.py.",
        )
        raise ExtensionError(
            msg,
        ) from None

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


def datatables_options_to_js(options: dict | str, indent: str) -> str:
    """
    Convert a Python nested dictionary to a valid JS dictionary object as a str.

    If it's a string already, dedent and return. It will also append a comma at
    the end if not already present.
    """
    if isinstance(options, dict):
        obj = json.dumps(options, indent=INDENT)
    else:  # If it's not a dict, just return whatever it is (e.g., a string)
        obj = textwrap.dedent(options)
    # prepend an indent to each line
    obj = "\n".join([indent + line for line in obj.splitlines()])
    if not obj.endswith(","):
        obj += ","
    return obj


def create_datatables_js(
    datatables_class: str,
    datatables_options: dict | str,
    datatables_version: str,
) -> str:
    """Create the JS file to activate datatables."""
    custom_file = Path(__file__).parent.joinpath("activate_datatables.js.in").absolute()
    with custom_file.open() as template:
        contents = template.read()
        contents = contents.replace(r"${datatables_class}", datatables_class)
        datatables_options = datatables_options_to_js(datatables_options, INDENT * 2)
        datatables_options = datatables_options.replace(
            r"${datatables_version}",
            datatables_version,
        )
        return contents.replace(r"${datatables_options}", datatables_options)


def finish(app: Sphinx, _exception: Exception | None) -> None:
    """
    Save the assets to the static directory.

    This function is called as the build finishes.

    Args:
        app (Sphinx): Sphinx app
        _exception (Exception | None): Any exceptions from the build

    """
    config = get_config(app)
    datatables_config_contents = create_datatables_js(
        config.datatables_class,
        config.datatables_options,
        config.datatables_version,
    )
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

    app.connect("html-page-context", add_datatables_scripts)
    app.connect("build-finished", finish)

    return {
        "version": importlib.metadata.version("sphinx_datatables"),
        "env_version": None,  # unset := no cache versioning required by this extension
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
