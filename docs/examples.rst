..
    Copyright (c) 2023 Varun Sharma

    SPDX-License-Identifier: MIT

Examples
########

This page shows some examples of tables you can make with ``sphinx_datatables``.
Underneath each table, the ``.rst`` code used to define the table is provided as a reference.

Defining a table
****************

You can define a simple table using any basic table definition role available in RST: ``list-table``, ``csv-table``, ``table``.
Here is the same table defined with each role.

.. table:: Title
    :class: sphinx-datatable

    =================== =================== ===================
    Heading 1, column 1 Heading 2, column 2 Heading 3, column 3
    =================== =================== ===================
    Row 1, column 1     Row 1, column 2     Row 1, column 3
    Row 1, column 1     Row 2, column 2     Row 2, column 3
    =================== =================== ===================

Expand the code-blocks below to view the RST source to define this table using:

.. collapse:: the "table" role

    .. code-block:: rst

        .. table:: Title
            :class: sphinx-datatable

            =================== =================== ===================
            Heading 1, column 1 Heading 2, column 2 Heading 3, column 3
            =================== =================== ===================
            Row 1, column 1     Row 1, column 2     Row 1, column 3
            Row 1, column 1     Row 2, column 2     Row 2, column 3
            =================== =================== ===================

.. collapse:: the "list-table" role

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

.. collapse:: the "csv-table" role

    .. code-block:: rst

        .. csv-table:: Title
            :header: "Heading 1, column 1","Heading 2, column 2","Heading 3, column 3"
            :class: sphinx-datatable

            "Row 1, column 1","Row 1, column 2","Row 1, column 3"
            "Row 2, column 1","Row 2, column 2","Row 2, column 3"

These tables all use the global class ``sphinx-datatable`` which can be :ref:`configured <global_options>` for all instances in ``conf.py``.

A larger example
****************

With more data, this table better demonstrates more advanced features enabled by DataTables such as search, pagination and sorting:

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

.. collapse:: Click here to see the .rst source code

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

Per-table configuration
***********************

Specifying ``:widths:`` with DataTables between v2.0.0 and v2.3.3
resulted in `unexpected formatting`_, but v2.3.4 fixed this.

.. _unexpected formatting: https://github.com/sharm294/sphinx-datatables/issues/13

Setting column widths is one example of where :ref:`per-table directives <directives>` can be useful.
Here, we use a custom class and a per-table directive to set this table's columns to 20%, 30% and 50%, respectively:

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

.. collapse:: Click here to see the .rst source code

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
