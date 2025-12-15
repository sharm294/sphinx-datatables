# Copyright (c) 2025 Varun Sharma
#
# SPDX-License-Identifier: MIT

"""
Tests suite for sphinx-datatables
"""
import pytest

from sphinx_datatables.sphinx_datatables import create_datatables_js


@pytest.mark.parametrize(
    "inputs, expected_outputs",
    [
        (
            ("sphinx-datatable", {"paging": True, "searching": False}, "2.3.5"),
            """\

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
} );
""",
        ),
        (
            ("sphinx-datatable", {"paging": True, "searching": False}, "3.0.0"),
            """\
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
} );
""",
        ),
        (
            ("another-datatable", {}, "3.0.0"),
            """\
// Copyright (c) 2023 Varun Sharma
//
// SPDX-License-Identifier: MIT

$(document).ready( function () {
    $('table.another-datatable').DataTable(
        {},
    );
} );
""",
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
            """\
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
} );
""",
        ),
        (
            (
                "sphinx-datatable",
                """{
scrollY: 300,
paging: false
}
""",
                "2.3.5",
            ),
            """\
// Copyright (c) 2023 Varun Sharma
//
// SPDX-License-Identifier: MIT

$(document).ready( function () {
    $('table.sphinx-datatable').DataTable(
        {
        scrollY: 300,
        paging: false
        },
    );
} );""",
        ),
    ],
)
def test_create_datatables_js(inputs, expected_outputs):
    """
    Test the create_datatables_js function
    """
    datatables_class, datatables_options, datatables_version = inputs
    expected_output = expected_outputs.strip()
    result = create_datatables_js(
        datatables_class, datatables_options, datatables_version
    )
    assert result.strip() == expected_output
