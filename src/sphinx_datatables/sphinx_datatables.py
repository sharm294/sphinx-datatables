# Copyright (c) 2023 Varun Sharma
#
# SPDX-License-Identifier: MIT

import json
import os
import textwrap
from dataclasses import dataclass
from pathlib import Path
from typing import Union

import packaging.version
from docutils import nodes
from sphinx.application import Sphinx
from sphinx.errors import ExtensionError

INDENT = " " * 4


@dataclass
class Config:
    """
    Holds the configuration data for the extension
    """

    datatables_version: str
    datatables_class: str
    datatables_options: Union[dict, str]


def set_config(app: Sphinx):
    """
    Save the configuration data from the user to the environment for easy
    retrieval later

    Args:
        app (Sphinx): Sphinx app
    """
    app.env.datatables_config = Config(
        datatables_version=app.config.datatables_version,
        datatables_class=app.config.datatables_class,
        datatables_options=app.config.datatables_options,
    )


def get_config(app: Sphinx) -> Config:
    return app.env.datatables_config


def add_datatables_scripts(
    app: Sphinx,
    pagename: str,
    templatename: str,
    context: dict,
    doctree: nodes.document,
):
    """
    Add the scripts to enable Datatables
    """

    config = get_config(app)

    # Set up jQuery first, to verify it is available and gracefully output an error
    try:
        app.setup_extension("sphinxcontrib.jquery")
    except ExtensionError:
        raise ExtensionError(
            "sphinxcontrib.jquery is required for sphinx-datatables to work. "
            "Please add it to your extensions in conf.py."
        )

    datetables_version_str = config.datatables_version
    if packaging.version.parse(datetables_version_str) < packaging.version.parse("2.0.0"):
        datatables_js = f"https://cdn.datatables.net/{datetables_version_str}/js/jquery.dataTables.min.js"
        datatables_css = f"https://cdn.datatables.net/{datetables_version_str}/css/jquery.dataTables.min.css"
    else:  # this is for DataTables 2.0.0 and above, only the minified version is available (jQuery is not included)
        datatables_js = f"https://cdn.datatables.net/v/dt/dt-{datetables_version_str}/datatables.min.js"
        datatables_css = f"https://cdn.datatables.net/v/dt/dt-{datetables_version_str}/datatables.min.css"

    app.add_js_file(datatables_js)
    app.add_css_file(datatables_css)
    app.add_js_file("activate_datatables.js")


def datatables_options_to_js(options: Union[dict, str], indent: str):
    """
    Convert a Python nested dictionary to a valid JS dictionary object as a string
    or the string itself if it's not a dict, but indented.
    Appends a comma at the end if not already present.
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
    datatables_class: str, datatables_options: Union[dict, str], datatables_version: str
) -> str:
    """
    Create the JS file to activate datatables
    """
    custom_file = str(
        Path(__file__).parent.joinpath("activate_datatables.js").absolute()
    )
    with open(custom_file + ".in", "r") as template:
        contents = template.read()
        contents = contents.replace(r"${datatables_class}", datatables_class)
        datatables_options = datatables_options_to_js(datatables_options, INDENT * 2)
        datatables_options = datatables_options.replace(
            r"${datatables_version}", datatables_version
        )
        contents = contents.replace(r"${datatables_options}", datatables_options)
    return contents


def finish(app: Sphinx, exception):
    config = get_config(app)
    datatables_config_contents = create_datatables_js(
        config.datatables_class,
        config.datatables_options,
        config.datatables_version,
    )
    asset_file = os.path.join(app.builder.outdir, "_static/activate_datatables.js")
    with open(asset_file, "w+") as f:
        f.write(datatables_config_contents)


def setup(app: Sphinx):
    """
    Setup the extension

    Args:
        app (Sphinx): Sphinx app
    """

    app.add_config_value("datatables_version", "2.3.5", "html", str)
    app.add_config_value("datatables_class", "sphinx-datatable", "html", str)
    app.add_config_value("datatables_options", {}, "html", [dict, str])

    app.connect("builder-inited", set_config)
    app.connect("html-page-context", add_datatables_scripts)
    app.connect("build-finished", finish)
