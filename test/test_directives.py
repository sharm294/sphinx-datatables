# Copyright (c) 2025 Varun Sharma
#
# SPDX-License-Identifier: MIT

"""Directive tests for sphinx-datatables."""

import sys
import textwrap
from io import StringIO
from pathlib import Path

import pytest
from sphinx.testing.util import SphinxTestApp

from .conftest import SphinxTestPath

NL = "\n"


@pytest.mark.parametrize("use_path", [None, "", "../", "foo/"])
@pytest.mark.parametrize("kind", ["json", "toml", "js"])
def test_json_directive(
    kind: str, use_path: str | None, basic_site: Path, tmp_path: Path
) -> None:
    """Test the expected output from the JSON directive."""
    build = tmp_path / "build"
    index_rst = basic_site / "index.rst"
    table = textwrap.dedent("""
        test
        ====

        .. table:: Title
            :class: custom-datatable

            =================== =================== ===================
            Heading 1, column 1 Heading 2, column 2 Heading 3, column 3
            =================== =================== ===================
            Row 1, column 1     Row 1, column 2     Row 1, column 3
            =================== =================== ===================""")
    if kind == "json":
        content = """{"searching": false}"""
    elif kind == "toml":
        content = """searching = false"""
    elif kind == "js":
        content = """;(function(){ return {searching: !!0}; }).call(this),"""

    if use_path is not None:
        path = basic_site / use_path / f"datatables.{kind}"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        body = f":path: {use_path}{path.name}"
    else:
        body = f"{NL}            {content}"

    directive = textwrap.dedent(f"""
        .. datatables-{kind}:: table.custom-datatable
            {body}""")

    rst_content = f"{table}{NL * 2}{directive}"
    print(rst_content)  # noqa: T201

    index_rst.write_text(rst_content, encoding="utf-8")
    io = StringIO()
    app = SphinxTestApp(
        "html",
        SphinxTestPath(basic_site),
        SphinxTestPath(build),
        status=io,
    )
    app.build()
    sys.stderr.write(f"{NL}{io.getvalue()}{NL}")
    assert app.statuscode == 0
    index_html = (build / "html/index.html").read_text(encoding="utf-8")
    assert (
        "$(`table.custom-datatable`).filter(':not(.dataTable)').DataTable("
        in index_html
    )
