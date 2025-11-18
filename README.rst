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
        "sphinxcontrib.jquery",
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


.. note::
    By using ``DataTables`` you are introducing many features that will have side-effects
    on the resulting HTML live rendering (as it is JavaScript based). So please,
    bear in mind that ``Sphinx`` features or your custom styles may not be compatible with
    it.

    ``DataTables`` provides many features that can be tweaked at its configuration.

    For example, starting with ``DataTables v2``, it calculates it's optimal column widths
    by default, messing with any user-specified ``:widths:`` in the table directive.
    In ``DataTables v2.3.4`` a change was published that completely overrides this config,
    so as to avoid this duplication and messing with the rendering. However, note that
    there is a configuration field in ``DataTables``, that, if needed, could be set to
    manually specify the widths. See `columns.width <https://datatables.net/reference/option/columns.width>`__.

.. note::
    You may want to add this package as a documentation dependency to your setup procedure.
    As any other semver-following project, it is suggested to pin the version for reproducibility and not breaking the build process once there are
    releases with breaking changes.

    You can either specify the exact dependency as ``sphinx-datatables==x.y.z`` or
    as a `PEP440 Compatible Release <https://peps.python.org/pep-0440/#compatible-release>`__,
    ``sphinx-datatables~=x.y.z``. The latter will match ``x.y.a / a >= z``
    stable releases; only patches will make it into your doc build process.

Configuration
-------------

The following configuration options are available with the following default values:

.. code-block:: python

    # in conf.py

    # set the version to use for DataTables plugin
    datatables_version = "2.3.5"

    # name of the class to use for tables to enable DataTables
    datatables_class = "sphinx-datatable"

    # any custom options to pass to the DataTables constructor. Note that any
    # options you set are used for all DataTables.
    datatables_options = {}
