# Copyright (c) 2023 Varun Sharma
#
# SPDX-License-Identifier: MIT

import os
from dataclasses import dataclass
from pathlib import Path

from docutils import nodes
from sphinx.application import Sphinx
from sphinx.util.fileutil import copy_asset_file


@dataclass
class Config:
    """
    Holds the configuration data for the extension
    """

    datatables_version: str
    datatables_class: str


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

    datatables_js = f"https://cdn.datatables.net/{config.datatables_version}/js/jquery.dataTables.min.js"
    datatables_css = f"https://cdn.datatables.net/{config.datatables_version}/css/jquery.dataTables.min.css"

    app.add_js_file(datatables_js)
    app.add_css_file(datatables_css)
    app.add_js_file("activate_datatables.js")


def finish(app: Sphinx, exception):

    custom_file = str(
        Path(__file__).parent.joinpath("activate_datatables.js").absolute()
    )
    print("copying?")
    copy_asset_file(custom_file, os.path.join(app.builder.outdir, "_static"))


def setup(app: Sphinx):
    """
    Setup the extension

    Args:
        app (Sphinx): Sphinx app
    """

    app.add_config_value("datatables_version", "1.13.4", "html", str)
    app.add_config_value("datatables_class", "sphinx-datatables", "html", str)

    app.connect("builder-inited", set_config)
    app.connect("html-page-context", add_datatables_scripts)
    app.connect("build-finished", finish)
