..
    Copyright (c) 2026 Varun Sharma

    SPDX-License-Identifier: MIT

Configuration
#############

DataTables comes with many `options <https://datatables.net/reference/option/>`__.
By default, no options are set.

.. _global_options:

Global options
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

.. _directives:

Directives
**********

In addition to setting global options in ``conf.py``, the following directives
allow for configuring tables by DOM
`selector <https://developer.mozilla.org/en-US/docs/Web/CSS/Guides/Selectors>`__;
this can be:

* an ``#id``
* a ``.class``
* a more complex ``[attribute="selector"]``
* or a comma-separated list of any of the above

Each table will inherit the global defaults from ``datatables_options``, but can
override or add any further options.

.. note::  Selectors should be unique on a given page.

    If a directive selector overlaps
    with another selector, only the first one defined will take effect. This
    includes the default selector generated from ``datatables_class``, which will
    always resolve first.

``datatables-json``
===================

Configure the tables on a page by providing a selector and any other values via
valid JSON.

.. code-block:: rst

    .. datatables-json::  table.custom-table

        {
            "searching": false
        }

.. _path-option:

``:path:``
----------

Use the ``:path:`` option to load ``DataTables`` options from
a JSON file at build time.

.. code-block:: rst

    .. datatables-json::  table.custom-table
        :path:  ../path/to/data/tables.json

``datatables-toml``
===================

Configure the tables on a page by providing a selector and any other values via
valid TOML. The :ref:`path-option` option is also supported.

.. code-block:: rst

    .. datatables-toml::  table.another-custom-table, table.still-another-selector

        searching = false

.. note::

    This requires Python 3.11+, or the ``tomli`` library.

``datatables-js``
=================

Configure the tables on a page by providing a selector and any other
values via JavaScript. The :ref:`path-option` option is also supported.

.. code-block:: rst

    .. datatables-js::  table.yet-another-custom-table

        {searching: false}


JavaScript provided this way must be an expression which returns a ``DataTable``
options object. For highly dynamic code, use an "immediately invoked function expression",
or `IIFE <https://developer.mozilla.org/en-US/docs/Glossary/IIFE>`__:

.. code-block:: rst

    .. datatables-js::  table.custom-table

        ;(function() {
            return { searching: !!0 };
        }).call(this)

Custom assets
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
