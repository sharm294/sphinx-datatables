# Copyright (c) 2023 Varun Sharma
#
# SPDX-License-Identifier: MIT

import importlib.metadata
import json
import os
import textwrap
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Union

import jinja2
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
    datatables_js: str
    datatables_css: str
    datatables_selector_options: Dict[str, Union[dict, str]]


def get_config(app: Sphinx) -> Config:
    return Config(
        datatables_version=app.config.datatables_version,
        datatables_class=app.config.datatables_class,
        datatables_options=app.config.datatables_options,
        datatables_js=app.config.datatables_js,
        datatables_css=app.config.datatables_css,
        datatables_selector_options=app.config.datatables_selector_options,
    )


def add_datatables_scripts(
    app: Sphinx,
    pagename: str,
    templatename: str,
    context: dict,
    doctree: nodes.document,
) -> None:
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
    if packaging.version.parse(datetables_version_str) < packaging.version.parse(
        "2.0.0"
    ):
        datatables_js = f"https://cdn.datatables.net/{datetables_version_str}/js/jquery.dataTables.min.js"
        datatables_css = f"https://cdn.datatables.net/{datetables_version_str}/css/jquery.dataTables.min.css"
    else:  # this is for DataTables 2.0.0 and above, only the minified version is available (jQuery is not included)
        datatables_js = f"https://cdn.datatables.net/v/dt/dt-{datetables_version_str}/datatables.min.js"
        datatables_css = f"https://cdn.datatables.net/v/dt/dt-{datetables_version_str}/datatables.min.css"

    if config.datatables_js:
        datatables_js = config.datatables_js

    if config.datatables_css:
        datatables_css = config.datatables_css

    app.add_js_file(datatables_js)
    app.add_css_file(datatables_css)
    app.add_js_file("activate_datatables.js")


def datatables_options_to_js(options: Union[dict, str], indent: str) -> str:
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
    datatables_class: str,
    datatables_options: Union[dict, str],
    datatables_version: str,
    *,
    datatables_selector_options: Union[dict[str, Any], None] = None,
) -> str:
    """
    Create the JS file to activate datatables
    """
    custom_file = Path(__file__).parent.joinpath("activate_datatables.js.in")
    template = jinja2.Template(custom_file.read_text(encoding="utf-8"))
    selector_js = {
        selector: datatables_options_to_js(options, INDENT * 2)
        for selector, options in (datatables_selector_options or {}).items()
    }

    rendered = template.render(
        datatables_options=datatables_options_to_js(datatables_options, INDENT * 2),
        datatables_class=datatables_class,
        datatables_selector_options=selector_js,
    )

    return rendered.replace(r"${datatables_version}", datatables_version)


def finish(app: Sphinx, exception) -> None:
    config = get_config(app)
    datatables_config_contents = create_datatables_js(
        config.datatables_class,
        config.datatables_options,
        config.datatables_version,
        datatables_selector_options=config.datatables_selector_options,
    )
    asset_file = os.path.join(app.builder.outdir, "_static/activate_datatables.js")
    with open(asset_file, "w+") as f:
        f.write(datatables_config_contents)


def setup(app: Sphinx) -> dict[str, Any]:
    """
    Setup the extension

    Args:
        app (Sphinx): Sphinx app
    """

    app.add_config_value("datatables_version", "2.3.5", "html", str)
    app.add_config_value("datatables_class", "sphinx-datatable", "html", str)
    app.add_config_value("datatables_options", {}, "html", [dict, str])
    app.add_config_value("datatables_js", "", "html", str)
    app.add_config_value("datatables_css", "", "html", str)
    app.add_config_value("datatables_selector_options", {}, "html", dict)

    app.connect("html-page-context", add_datatables_scripts)
    app.connect("build-finished", finish)

    return {
        "version": importlib.metadata.version("sphinx_datatables"),
        "env_version": None,  # unset := no cache versioning required by this extension
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
