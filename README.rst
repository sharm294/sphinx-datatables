..
    Copyright (c) 2023 Varun Sharma

    SPDX-License-Identifier: MIT

Sphinx DataTables
=================

This extension makes it easy to use more expressive tables in Sphinx documentation with `DataTables <https://datatables.net/>`__.
See the demo and full documentation `online <https://sharm294.github.io/sphinx-datatables/>`__.

Installation
------------

.. code-block:: console

    pip install sphinx-datatables

Usage
-----

Add the extension in your ``conf.py``:

.. code-block:: python

    extensions = [
        "sphinx_datatables",
    ]

In your ``.rst`` documentation, create a table and add a custom class label.
Your table must have a valid header row.

.. code-block:: rst

    .. csv-table::
        :header: First Name,Last Name
        :class: sphinx-datatable

        John,Smith
        Jane,Doe

Configuration
-------------

The following configuration options are available with the following default values:

.. code-block:: python

    # in conf.py

    # set the version to use for DataTables plugin
    datatables_version = "2.3.0"

    # name of the class to use for tables to enable DataTables
    datatables_class = "sphinx-datatable"

    # any custom options to pass to the DataTables constructor. Note that any
    # options you set are used for all DataTables.
    datatables_options = {}
