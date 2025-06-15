# Copyright (c) 2023 Varun Sharma
#
# SPDX-License-Identifier: MIT

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any
import importlib.metadata

from docutils import nodes
from sphinx.application import Sphinx

INDENT = " " * 4


@dataclass
class Config:
    """
    Holds the configuration data for the extension
    """
    datatables_version: str
    datatables_class: str
    datatables_options: dict


def get_config(app: Sphinx) -> Config:
    return Config(
        datatables_version=app.config.datatables_version,
        datatables_class=app.config.datatables_class,
        datatables_options=app.config.datatables_options,
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

    datatables_js = f"https://cdn.datatables.net/{config.datatables_version}/js/jquery.dataTables.min.js"
    datatables_css = f"https://cdn.datatables.net/{config.datatables_version}/css/jquery.dataTables.min.css"

    app.add_js_file(datatables_js)
    app.add_css_file(datatables_css)
    app.add_js_file("activate_datatables.js")


def dict_to_js(options: dict, version: str, indent: str):
    """
    Convert a Python nested dictionary to a valid JS dictionary object as a string
    """

    obj = indent + "{\n"
    for key, value in options.items():
        if isinstance(value, dict):
            value_str = dict_to_js(value, version, indent + INDENT)
        elif isinstance(value, str):
            value_str = f"'{value},'"
            value_str = value_str.replace(r"${datatables_version}", version)
        else:
            value_str = f"{value},"
        obj += f"{indent + INDENT}{key}: {value_str}\n"
    obj += indent + "},\n"
    return obj


def finish(app: Sphinx, exception):

    custom_file = str(
        Path(__file__).parent.joinpath("activate_datatables.js").absolute()
    )
    config = get_config(app)
    with open(custom_file + ".in", "r") as template:
        contents = template.read()
        contents = contents.replace(r"${datatables_class}", config.datatables_class)
        datatables_options = dict_to_js(
            config.datatables_options, config.datatables_version, INDENT * 2
        )
        contents = contents.replace(r"${datatables_options}", datatables_options)
        asset_file = os.path.join(app.builder.outdir, "_static/activate_datatables.js")
        with open(asset_file, "w+") as f:
            f.write(contents)


def setup(app: Sphinx) -> dict[str, Any]:
    """
    Setup the extension

    Args:
        app (Sphinx): Sphinx app
    """

    app.add_config_value("datatables_version", "1.13.4", "html", str)
    app.add_config_value("datatables_class", "sphinx-datatable", "html", str)
    app.add_config_value("datatables_options", {}, "html", dict)

    app.connect("html-page-context", add_datatables_scripts)
    app.connect("build-finished", finish)

    return {
        "version": importlib.metadata.version("sphinx_datatables"),
        "env_version": 0,  # 0 := no environment versioning needed since this extension does not store state except for the config values
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
