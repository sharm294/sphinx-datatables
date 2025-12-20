# Copyright (c) 2025 Varun Sharma
#
# SPDX-License-Identifier: MIT

"""Tests suite for sphinx-datatables."""

import importlib.metadata
import textwrap
from pathlib import Path
from typing import Any

import pytest
from packaging.version import Version
from sphinx.testing.util import SphinxTestApp

from sphinx_datatables.sphinx_datatables import create_datatables_js

if Version(importlib.metadata.version("sphinx")) >= Version("7"):
    SphinxTestPath = Path
else:
    from sphinx.testing.path import path as SphinxTestPath  # noqa: N812


@pytest.mark.parametrize(
    ("inputs", "expected_outputs"),
    [
        (
            ("sphinx-datatable", {"paging": True, "searching": False}, "2.3.5"),
            textwrap.dedent("""
                // Copyright (c) 2023 Varun Sharma
                //
                // SPDX-License-Identifier: MIT

                $(document).ready( function () {
                    $('table.sphinx-datatable').DataTable(
                        {
                            "paging": true,
                            "searching": false
                        },
                    );
                } );"""),
        ),
        (
            ("sphinx-datatable", {"paging": True, "searching": False}, "3.0.0"),
            textwrap.dedent("""
                // Copyright (c) 2023 Varun Sharma
                //
                // SPDX-License-Identifier: MIT

                $(document).ready( function () {
                    $('table.sphinx-datatable').DataTable(
                        {
                            "paging": true,
                            "searching": false
                        },
                    );
                } );"""),
        ),
        (
            ("another-datatable", {}, "3.0.0"),
            textwrap.dedent("""\
                // Copyright (c) 2023 Varun Sharma
                //
                // SPDX-License-Identifier: MIT

                $(document).ready( function () {
                    $('table.another-datatable').DataTable(
                        {},
                    );
                } );"""),
        ),
        (
            (
                "sphinx-datatable",
                {
                    "pageLength": -1,
                    "language": {"lengthLabels": {"-1": "Show all"}},
                    "lengthMenu": [10, 25, 50, -1],
                },
                "2.3.5",
            ),
            textwrap.dedent("""
                // Copyright (c) 2023 Varun Sharma
                //
                // SPDX-License-Identifier: MIT

                $(document).ready( function () {
                    $('table.sphinx-datatable').DataTable(
                        {
                            "pageLength": -1,
                            "language": {
                                "lengthLabels": {
                                    "-1": "Show all"
                                }
                            },
                            "lengthMenu": [
                                10,
                                25,
                                50,
                                -1
                            ]
                        },
                    );
                } );"""),
        ),
        (
            (
                "sphinx-datatable",
                {"scrollY": 300, "paging": False},
                "2.3.5",
            ),
            textwrap.dedent("""
                // Copyright (c) 2023 Varun Sharma
                //
                // SPDX-License-Identifier: MIT

                $(document).ready( function () {
                    $('table.sphinx-datatable').DataTable(
                        {
                            "scrollY": 300,
                            "paging": false
                        },
                    );
                } );"""),
        ),
    ],
)
def test_create_datatables_js(
    inputs: tuple[str, dict[str, Any], str],
    expected_outputs: str,
) -> None:
    """Test the create_datatables_js function."""
    datatables_class, datatables_options, datatables_version = inputs
    expected_output = expected_outputs.strip()
    result = create_datatables_js(
        datatables_class,
        datatables_options,
        datatables_version,
    )
    assert result.strip() == expected_output


@pytest.mark.parametrize("add_js", [True, False])
@pytest.mark.parametrize("add_css", [False, True])
def test_custom_js_css(
    tmp_path: Path,
    basic_site: Path,
    add_js: bool,
    add_css: bool,
) -> None:
    """Test custom JS/CSS ends up in the built output when configured."""
    build = tmp_path / "build"
    _static = basic_site / "_static"
    conf_lines: list[str] = []

    if add_js:
        test_js = _static / "test.js"
        conf_lines += [f"datatables_js = '{test_js.name}'"]

    if add_css:
        test_css = _static / "test.css"
        conf_lines += [f"datatables_css = '{test_css.name}'"]

    if conf_lines:
        conf_py = basic_site / "conf.py"
        conf_py.write_text(
            "\n".join([conf_py.read_text(encoding="utf-8"), *conf_lines]),
            encoding="utf-8",
        )

    app = SphinxTestApp("html", SphinxTestPath(basic_site), SphinxTestPath(build))
    app.build()

    index_html = (build / "html/index.html").read_text(encoding="utf-8")

    if add_js:
        assert f"_static/{test_js.name}" in index_html

    if add_css:
        assert f"_static/{test_css.name}" in index_html

    if add_js and add_css:
        assert "cdn.datatables.net" not in index_html


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
