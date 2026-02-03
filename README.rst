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

    Using ``DataTables`` introduces JavaScript and CSS side-effects in the DOM rendered in a site visitor's browser.

Usage
*****

In your ``.rst`` documentation, create a table and add a custom class.
The default class, ``sphinx-datatable``, can be overriden in ``conf.py`` with the ``datatables_class`` option.

Each table must have a valid header row.

.. code-block:: rst

    .. csv-table::
        :header: First Name,Last Name
        :class: sphinx-datatable

        John,Smith
        Jane,Doe

``DataTables`` provides many `options <https://datatables.net/reference/option>`__ that can be configured globally in ``conf.py`` with ``datatables_options``.
You can also configure specific per-table (or tables) on any page that match a DOM selector with the directives.

See the documentation for more examples and details on per-table configuration.

Contributions
*************

Contributions are welcome if there's a feature or bug you find.
Please raise an issue first to discuss the request.

To submit a PR, fork this repository and make a branch with your changes.
You can test the project locally with:

.. code-block:: bash

    # install all dependencies
    pip install .[docs,dev]

    # build the docs locally
    ./docs/build.sh
    # you can use a local browser to the build/ directory to view the HTML docs

    # run the tests
    pytest
