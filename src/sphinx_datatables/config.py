# Copyright (c) 2023 Varun Sharma
#
# SPDX-License-Identifier: MIT

"""Typed configuration."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from sphinx.config import Config as SphinxConfig


@dataclass
class SphinxDatatablesConfig:
    """Holds the configuration data for the extension."""

    datatables_version: str
    datatables_class: str
    datatables_options: dict | str = field(default_factory=dict)
    datatables_js: str = ""
    datatables_css: str = ""

    @classmethod
    def from_sphinx_config(cls, sphinx_config: SphinxConfig) -> SphinxDatatablesConfig:
        """Create SphinxDatatablesConfig from Sphinx-loaded configuration."""
        return cls(
            datatables_version=sphinx_config.datatables_version,
            datatables_class=sphinx_config.datatables_class,
            datatables_options=sphinx_config.datatables_options,
            datatables_js=sphinx_config.datatables_js,
            datatables_css=sphinx_config.datatables_css,
        )
