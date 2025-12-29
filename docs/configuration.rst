Custom Options
##############

DataTables comes with many `options <https://datatables.net/reference/option/>`__.
By default, no options are set.

Global Options
**************

If you want to change any of the options for *all* tables, use the ``datatables_options``
configuration option in ``conf.py``.

For example, to set the `internationalization plugin <https://datatables.net/plug-ins/i18n/>`__:

.. code-block:: python

    # in conf.py
    datatables_options = {
        "language": {
            "url": "https://cdn.datatables.net/plug-ins/${datatables_version}/i18n/fr-FR.json"
        }
    }
    # this is equivalent to JavaScript:
    datatables_options = """
    {
        language: {
            url: 'https://cdn.datatables.net/plug-ins/${datatables_version}/i18n/fr-FR.json,'
        },
    }"""

You can use the special variable ``${datatables_version}`` to dynamically set the DataTables version in URLs (which is substituted by ``datatables_version`` configuration value from ``conf.py``).

If it's a dictionary, then it is converted to JSON with `json.dumps <https://docs.python.org/3/library/json.html#json.dumps>`__ and passed to the JavaScript DataTables constructor.
If it's a string, it will be passed as is, so it will need to be a valid JavaScript string.

You can set any options you want, but make sure to follow the DataTables documentation for the correct format.
For example, if you want to set the ``pageLength`` option to ``-1`` (i.e., show all content), plus rename that option to ``Show all``, you would do it like this:

.. code-block:: python

    # in conf.py
    # as a dictionary
    datatables_options = {
        "pageLength": -1,
        "language": {"lengthLabels": {"-1": "Show all"}},
        "lengthMenu": [10, 25, 50, -1],
    }
    # as plain JavaScript in a string
    datatables_options = """{
        pageLength: -1,
        language: {
            lengthLabels: {
                '-1': 'Show all'
            }
        },
        lengthMenu: [10, 25, 50, -1]
        }"""


Custom Assets
*************

The default JavaScript and CSS assets are fetched from ``https://cdn.datatables.net``
at page load time, without any plugins enabled.

To start building custom bundles, use the three step
`download builder <https://datatables.net/download>`__
which provides, among other things:

* styles for CSS frameworks, such as Bootstrap
* enhanced search behavior
* customized download formats, including PDF

After making selections in step one and two, use one of the download techniques
in step three, and configure the ``datatables_js`` and ``datables_css`` options:

* Get remote URLs to load dynamic assets from `CDN`

    .. code-block:: python

        # conf.py
        datables_css = "https://cdn.datatables.net/v/dt/dt-2.3.5/datatables.min.css"
        datables_js  = "https://cdn.datatables.net/v/dt/dt-2.3.5/datatables.min.js"

* `Download` a ``.zip`` file and place the unzipped contents somewhere on ``html_static_paths``,
  conventionally `_static/vendor/datatables`

    .. code-block:: python

        # conf.py
        html_static_paths = ["_static"]
        datables_css = "vendor/datatables/datatables.min.css"
        datables_js  = "vendor/datatables/datatables.min.js"

* Use one of the more advanced package manager approaches, such as ``npm``,
  if appropriate for your site. These generated locations for ``datatables_js``
  and ``datatable_css`` will vary based on the tool.

Column Widths
*************

Specifying ``:widths:`` with DataTables between v2.0.0 and v2.3.3
resulted in `unexpected formatting`_, but v2.3.4 fixed this.

.. _unexpected formatting: https://github.com/sharm294/sphinx-datatables/issues/13

To set column widths for a single table, provide a unique selector (such as with a ``:class:``):

.. code-block:: rst

    .. table:: Custom Widths
        :class: sphinx-datatable-20-30-50

        =================== =================== ===================
        Heading 1, column 1 Heading 2, column 2 Heading 3, column 3
        =================== =================== ===================
        Row 1, column 1     Row 1, column 2     Row 1, column 3
        Row 1, column 1     Row 2, column 2     Row 2, column 3
        =================== =================== ===================

    .. datatables-json::  table.sphinx-datatable-20-30-50

        {
            "columnDefs": [
                {"width": "20%", "targets": 0},
                {"width": "30%", "targets": 1},
                {"width": "50%", "targets": 2}
            ]
        }

The table should now appear with the expected column widths:

.. table:: Custom Widths
    :class: sphinx-datatable-20-30-50

    =================== =================== ===================
    Heading 1, column 1 Heading 2, column 2 Heading 3, column 3
    =================== =================== ===================
    Row 1, column 1     Row 1, column 2     Row 1, column 3
    Row 1, column 1     Row 2, column 2     Row 2, column 3
    =================== =================== ===================

.. datatables-json::  table.sphinx-datatable-20-30-50

    {
        "columnDefs": [
            {"width": "20%", "targets": 0},
            {"width": "30%", "targets": 1},
            {"width": "50%", "targets": 2}
        ]
    }
