"""Typed configuration."""

# Copyright (c) 2023 Varun Sharma
#
# SPDX-License-Identifier: MIT

from dataclasses import dataclass, field

from sphinx.config import Config as SphinxConfig


@dataclass
class Config:
    """Holds the configuration data for the extension."""

    datatables_version: str
    datatables_class: str
    datatables_options: dict | str = field(default_factory=dict)
    datatables_js: str = ""
    datatables_css: str = ""


def get_config(sphinx_config: SphinxConfig) -> Config:
    """
    Return the configurable options.

    Args:
        sphinx_config (SphinxConfig): Sphinx configuration

    Returns:
        Config: Dataclass for the config options

    """
    return Config(
        datatables_version=sphinx_config.datatables_version,
        datatables_class=sphinx_config.datatables_class,
        datatables_options=sphinx_config.datatables_options,
        datatables_js=sphinx_config.datatables_js,
        datatables_css=sphinx_config.datatables_css,
    )
