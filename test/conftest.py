"""Tests configuration for sphinx-datatables."""
# Copyright (c) 2025 Varun Sharma
#
# SPDX-License-Identifier: MIT

import importlib.metadata
import textwrap
from pathlib import Path

import pytest
from packaging.version import Version

__all__ = ["SphinxTestPath", "basic_site"]

if Version(importlib.metadata.version("sphinx")) >= Version("7"):
    SphinxTestPath = Path
else:
    from sphinx.testing.path import path as SphinxTestPath  # noqa: N812


@pytest.fixture
def basic_site(tmp_path: Path) -> Path:
    """Provide a basic site folder with a single page with a table and config."""
    src = tmp_path / "src"
    src.mkdir()

    _static = src / "_static"
    _static.mkdir()

    conf_py = src / "conf.py"
    conf_py.write_text(
        textwrap.dedent("""
            extensions = ["sphinxcontrib.jquery", "sphinx_datatables"]
            html_static_path = ["_static"]""").strip(),
        encoding="utf-8",
    )

    index_rst = src / "index.rst"
    index_rst.write_text(
        textwrap.dedent("""
            test
            ====

            .. table:: Title
                :class: sphinx-datatable

                =================== =================== ===================
                Heading 1, column 1 Heading 2, column 2 Heading 3, column 3
                =================== =================== ===================
                Row 1, column 1     Row 1, column 2     Row 1, column 3
                =================== =================== ===================""").strip(),
        encoding="utf-8",
    )
    return src
