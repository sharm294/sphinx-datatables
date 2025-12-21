"""Directive tests for sphinx-datatables."""
# Copyright (c) 2025 Varun Sharma
#
# SPDX-License-Identifier: MIT

import textwrap
from pathlib import Path

from sphinx.testing.util import SphinxTestApp

from .conftest import SphinxTestPath


def test_json_directive_(tmp_path: Path, basic_site: Path) -> None:
    """Test the expected output from the JSON directive."""
    build = tmp_path / "build"
    index_rst = basic_site / "index.rst"
    index_rst.write_text(
        textwrap.dedent("""
            test
            ====

            .. table:: Title
                :class: custom-datatable

                =================== =================== ===================
                Heading 1, column 1 Heading 2, column 2 Heading 3, column 3
                =================== =================== ===================
                Row 1, column 1     Row 1, column 2     Row 1, column 3
                =================== =================== ===================

            .. datatables-json::

                {"table.custom-datatable": {"searching": false}}""").strip(),
        encoding="utf-8",
    )
    app = SphinxTestApp("html", SphinxTestPath(basic_site), SphinxTestPath(build))
    app.build()
    assert app.statuscode == 0
    index_html = (build / "html/index.html").read_text(encoding="utf-8")
    assert "$(`table.custom-datatable`).DataTable(" in index_html
