..
    Copyright (c) 2023 Varun Sharma

    SPDX-License-Identifier: MIT

Sphinx DataTables
#################

This extension makes it easy to use more expressive tables in Sphinx site with `DataTables <https://datatables.net/>`__.
See the demo and full documentation `online <https://sharm294.github.io/sphinx-datatables/>`__.

Installation
************

.. code-block:: console

    pip install sphinx-datatables

Add the extension in your ``conf.py``:

.. code-block:: python

    extensions = [
        "sphinxcontrib.jquery",
        "sphinx_datatables",
    ]

.. note::

    Using ``DataTables`` introduces JavaScript and CSS side-effects in the
    DOM rendered in a site visitor's browser.

Usage
*****

In your ``.rst`` documentation, create a table and add a custom class.
The default class, ``sphinx-datatable``, (can be overriden in ``conf.py`` with
the ``datatables_class`` option).

Each table must have a valid header row.

.. code-block:: rst

    .. csv-table::
        :header: First Name,Last Name
        :class: sphinx-datatable

        John,Smith
        Jane,Doe

``DataTables`` provides many `options <https://datatables.net/reference/option>`__
that can be configured globally in ``conf.py`` with ``datatables_options``.

Configure options for a specific table (or tables) on any page that match a DOM
selector with the :ref:`directives` described below.

Configuration
*************

The following ``conf.py`` options are available with the following default values:

.. code-block:: python

    # in conf.py

    # set the version to use for DataTables plugin
    datatables_version = "2.3.5"

    # name of the class to use for tables to automatically enable DataTables
    datatables_class = "sphinx-datatable"

    # any custom options to pass to the DataTables constructor. Note that any
    # options you set are used for all DataTables.
    datatables_options = {}

    # custom remote URLs (or offline path in html_static_paths) for ...
    ## datatables.min.js
    datatables_js = ""
    ## datatables.min.css
    datatables_css = ""

.. _directives:

Directives
**********

In addition to setting global options in ``conf.py``, the following directives
allow for configuring tables by DOM
`selector <https://developer.mozilla.org/en-US/docs/Web/CSS/Guides/Selectors>`__;
this can be an ``#id``, a ``.class`` or a more complex ``[attribute="selector"]``.

Each table will inherit the global defaults from ``datatables_options``, but can
override or add any further options.

.. warning:

    Selectors configured this way should be unique on a given page.
    If two directives overlap on the same page (or with the ``datatables_class``),
    a browser alert will open.

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

    .. datatables-json::  table.another-custom-table, table.still-another-selector

        searching = false

.. note:

    This requires Python 3.11+, or the ``tomli`` library.

``datatables-js``
=================

Configure the tables on a page by providing a selector and any other
values via JavaScript. The ``:path:`` option is also supported.

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
