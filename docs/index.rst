..
    Copyright (c) 2023 Varun Sharma

    SPDX-License-Identifier: MIT

.. include:: ../README.rst

Examples
--------

``csv-table``
^^^^^^^^^^^^^

Using the ``csv-table`` role:

.. csv-table::
    :header: ID,First name,Last name,Birthdate,Added
    :class: sphinx-datatable

    1,Kaden,Labadie,1976-09-21,1970-10-20 12:52:05
    2,Ophelia,Klocko,2018-04-11,1983-10-04 12:02:17
    3,Ariel,Quigley,1990-10-19,2006-10-01 21:27:50
    4,Wilfredo,Kessler,2011-07-07,1985-08-18 01:23:32
    5,Malvina,Littel,1994-04-14,2010-08-06 03:07:54
    6,Ralph,Kassulke,1988-03-02,1977-02-28 13:09:11
    7,Karelle,Koelpin,1990-07-10,2012-12-30 10:01:10
    8,Tyson,Bradtke,1992-10-17,2020-05-28 04:30:24
    9,Micheal,Sporer,1987-06-26,2019-10-30 11:15:57
    10,Sheridan,Sawayn,1999-08-21,2008-07-01 12:22:34
    11,Keon,Tremblay,2004-05-22,1984-09-12 14:26:05
    12,Elisabeth,Stokes,1989-04-01,1995-09-14 11:48:33
    13,Gage,Schinner,1982-12-03,1975-06-17 11:55:43
    14,Erik,Cremin,2013-03-03,1996-09-24 15:14:34
    15,Retha,Spinka,2017-05-25,1982-08-25 00:42:26
    16,Odie,Windler,1993-10-14,1998-08-17 11:46:13
    17,Alexandrea,Fadel,2021-04-26,1984-08-13 23:02:20
    18,Brody,Luettgen,1981-11-02,1990-05-30 14:01:01
    19,Bernita,Stroman,1973-07-24,1981-09-10 21:58:27
    20,Zula,Greenholt,2019-06-07,2020-07-24 13:13:02

.. collapse:: Source code

    .. code-block:: rst

        .. csv-table::
            :header: ID,First name,Last name,Email,Birthdate,Added
            :class: sphinx-datatable

            1,Kaden,Labadie,1976-09-21,1970-10-20 12:52:05
            2,Ophelia,Klocko,2018-04-11,1983-10-04 12:02:17
            3,Ariel,Quigley,1990-10-19,2006-10-01 21:27:50
            4,Wilfredo,Kessler,2011-07-07,1985-08-18 01:23:32
            5,Malvina,Littel,1994-04-14,2010-08-06 03:07:54
            6,Ralph,Kassulke,1988-03-02,1977-02-28 13:09:11
            7,Karelle,Koelpin,1990-07-10,2012-12-30 10:01:10
            8,Tyson,Bradtke,1992-10-17,2020-05-28 04:30:24
            9,Micheal,Sporer,1987-06-26,2019-10-30 11:15:57
            10,Sheridan,Sawayn,1999-08-21,2008-07-01 12:22:34
            11,Keon,Tremblay,2004-05-22,1984-09-12 14:26:05
            12,Elisabeth,Stokes,1989-04-01,1995-09-14 11:48:33
            13,Gage,Schinner,1982-12-03,1975-06-17 11:55:43
            14,Erik,Cremin,2013-03-03,1996-09-24 15:14:34
            15,Retha,Spinka,2017-05-25,1982-08-25 00:42:26
            16,Odie,Windler,1993-10-14,1998-08-17 11:46:13
            17,Alexandrea,Fadel,2021-04-26,1984-08-13 23:02:20
            18,Brody,Luettgen,1981-11-02,1990-05-30 14:01:01
            19,Bernita,Stroman,1973-07-24,1981-09-10 21:58:27
            20,Zula,Greenholt,2019-06-07,2020-07-24 13:13:02

``list-table``
^^^^^^^^^^^^^^

Using the ``list-table`` role:

.. list-table:: Title
    :header-rows: 1
    :class: sphinx-datatable

    * - Heading 1, column 1
      - Heading 1, column 2
      - Heading 1, column 3
    * - Row 1, column 1
      - Row 1, column 2
      - Row 1, column 3
    * - Row 2, column 1
      - Row 2, column 2
      - Row 2, column 3

.. collapse:: Source code

    .. code-block:: rst

        .. list-table:: Title
            :header-rows: 1
            :class: sphinx-datatable

            * - Heading 1, column 1
              - Heading 1, column 2
              - Heading 1, column 3
            * - Row 1, column 1
              - Row 1, column 2
              - Row 1, column 3
            * - Row 2, column 1
              - Row 2, column 2
              - Row 2, column 3

``table``
^^^^^^^^^

Using the ``table`` role:

.. table:: Title
    :class: sphinx-datatable

    =================== =================== ===================
    Heading 1, column 1 Heading 2, column 2 Heading 3, column 3
    =================== =================== ===================
    Row 1, column 1     Row 1, column 2     Row 1, column 3
    Row 1, column 1     Row 2, column 2     Row 2, column 3
    =================== =================== ===================

.. collapse:: Source code

    .. code-block:: rst

        .. table:: Title
            :class: sphinx-datatable

            =================== =================== ===================
            Heading 1, column 1 Heading 2, column 2 Heading 3, column 3
            =================== =================== ===================
            Row 1, column 1     Row 1, column 2     Row 1, column 3
            Row 1, column 1     Row 2, column 2     Row 2, column 3
            =================== =================== ===================

Custom Options
--------------

DataTables comes with many `options <https://datatables.net/reference/option/>`__.
By default, no options are set.
If you want to change any of them, you can use the `datatables_options` configuration option in `conf.py`.
Note that all DataTables will share the same options you set here.

For example, to set the `internationalization plugin <https://datatables.net/plug-ins/i18n/>`__:

.. code-block:: python

    # in conf.py
    datatables_options = {
        "language": {
            "url": "https://cdn.datatables.net/plug-ins/${datatables_version}/i18n/fr-FR.json"
        }
    }
    # this is equivalent to JavaScript:
    datatables_options = """\
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


Column Widths
-------------

Since DataTables v2.0.0, it is no longer possible to set column widths
via ``:widths:``, e.g.,

.. code-block:: rst

   .. csv-table:: Title
      :class: sphinx-datatable
      :file: data.csv
      :header-rows: 1
      :widths: 20,30,50

Specifying ``:widths:`` with DataTables between v2.0.0 and v2.3.3
resulted in `unexpected formatting`_, but v2.3.4 fixed this.  If you
still wish to control your column widths, you can do so with

.. code-block:: python

   datatables_options = {
       "columnDefs": [
           {"width": "20%", "targets": 0},
           {"width": "30%", "targets": 1},
           {"width": "50%", "targets": 2},
       ]

in your ``conf.py``, but that will apply to all ``sphinx-datatable``
tables in your site.

.. _unexpected formatting: https://github.com/sharm294/sphinx-datatables/issues/13

Custom Selectors
----------------

To set options for *only* a specific table or tables, use ``datatables_selector_options``,
a dictionary of DataTables options keyed by CSS selectors. These values will
be merged with the default values configured in ``datatables_options``.

.. code-block:: python

    # in conf.py
    datatables_selector_options = {
        # the effective default behavior uses ``datatables_options``
        # "table.sphinx-datatable": {}
        # per selector options
        "table.a-table": {
            "title": ["A", "B", "C"]
        },
        "table.another-table, .table#yet-another-table": {
            "title": ["X", "Y", "Z"]
        }
    }
