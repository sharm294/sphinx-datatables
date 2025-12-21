# Copyright (c) 2025 Varun Sharma
#
# SPDX-License-Identifier: MIT

"""Tests suite for sphinx-datatables."""

import textwrap
from pathlib import Path
from typing import Any

import pytest
from sphinx.testing.util import SphinxTestApp

from sphinx_datatables.config import Config
from sphinx_datatables.js import create_datatables_js

from .conftest import SphinxTestPath


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
        Config(
            datatables_class=datatables_class,
            datatables_options=datatables_options,
            datatables_version=datatables_version,
        )
    )
    assert result.strip() == expected_output


@pytest.mark.parametrize(
    ("inputs", "expected_outputs"),
    [
        # single selector
        (
            {
                "datatables_options": {"paging": True},
                "datatables_selector_options": {
                    """.custom-selector[data-attr="value"]""": {"searching": False}
                },
            },
            """\
// Copyright (c) 2023 Varun Sharma
//
// SPDX-License-Identifier: MIT

$(document).ready( function () {
    $.extend( $.fn.dataTable.defaults,
        {
            "paging": true
        },
    );

    $(`table.sphinx-datatable`).DataTable();

    $(`.custom-selector[data-attr="value"]`).DataTable(
        {
            "searching": false
        },
    );
} );""",
        ),
        # single selector, no default
        (
            {
                "datatables_class": "",
                "datatables_options": {"paging": True},
                "datatables_selector_options": {
                    """.custom-selector[data-attr="value"]""": "{searching: false},"
                },
            },
            """\
// Copyright (c) 2023 Varun Sharma
//
// SPDX-License-Identifier: MIT

$(document).ready( function () {
    $.extend( $.fn.dataTable.defaults,
        {
            "paging": true
        },
    );

    $(`.custom-selector[data-attr="value"]`).DataTable(
        {searching: false},
    );
} );""",
        ),
        # multiple selectors, version flag
        (
            {
                "datatables_options": {
                    "language": {
                        "url": "https://cdn.datatables.net/plug-ins/${datatables_version}/i18n/fr-FR.json"
                    }
                },
                "datatables_selector_options": {
                    """.custom-selector[data-attr="value"]""": "{searching: false},",
                    """.another-custom-selector""": {"searching": True},
                },
            },
            """\
// Copyright (c) 2023 Varun Sharma
//
// SPDX-License-Identifier: MIT

$(document).ready( function () {
    $.extend( $.fn.dataTable.defaults,
        {
            "language": {
                "url": "https://cdn.datatables.net/plug-ins/2.3.5/i18n/fr-FR.json"
            }
        },
    );

    $(`table.sphinx-datatable`).DataTable();

    $(`.custom-selector[data-attr="value"]`).DataTable(
        {searching: false},
    );

    $(`.another-custom-selector`).DataTable(
        {
            "searching": true
        },
    );
} );""",
        ),
    ],
)
def test_create_datables_js_selectors(
    inputs: dict[str, Any], expected_outputs: str
) -> None:
    """Test the create_datatables_js function with per-table options."""
    expected_output = expected_outputs.strip()
    config_kwargs = {
        "datatables_class": "sphinx-datatable",
        "datatables_version": "2.3.5",
    }
    config_kwargs.update(inputs)
    result = create_datatables_js(Config(**config_kwargs))
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
    assert app.statuscode == 0

    index_html = (build / "html/index.html").read_text(encoding="utf-8")

    if add_js:
        assert f"_static/{test_js.name}" in index_html

    if add_css:
        assert f"_static/{test_css.name}" in index_html

    if add_js and add_css:
        assert "cdn.datatables.net" not in index_html
