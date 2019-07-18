========
Overview
========

.. start-badges

.. list-table::
    :stub-columns: 1

    * - docs
      - |docs|
    * - tests
      - | |travis| |appveyor|
        |
    * - package
      - | |version| |wheel| |supported-versions| |supported-implementations|
        | |commits-since|

.. |docs| image:: https://readthedocs.org/projects/mario-addons/badge/?style=flat
    :target: https://readthedocs.org/projects/mario-addons
    :alt: Documentation Status


.. |travis| image:: https://travis-ci.org/python-mario/mario-addons.svg?branch=master
    :alt: Travis-CI Build Status
    :target: https://travis-ci.org/python-mario/mario-addons

.. |appveyor| image:: https://ci.appveyor.com/api/projects/status/github/python-mario/mario-addons?branch=master&svg=true
    :alt: AppVeyor Build Status
    :target: https://ci.appveyor.com/project/python-mario/mario-addons

.. |version| image:: https://img.shields.io/pypi/v/mario-addons.svg
    :alt: PyPI Package latest release
    :target: https://pypi.org/pypi/mario-addons

.. |commits-since| image:: https://img.shields.io/github/commits-since/python-mario/mario-addons/v0.1.0.svg
    :alt: Commits since latest release
    :target: https://github.com/python-mario/mario-addons/compare/v0.1.0...master

.. |wheel| image:: https://img.shields.io/pypi/wheel/mario-addons.svg
    :alt: PyPI Wheel
    :target: https://pypi.org/pypi/mario-addons

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/mario-addons.svg
    :alt: Supported versions
    :target: https://pypi.org/pypi/mario-addons

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/mario-addons.svg
    :alt: Supported implementations
    :target: https://pypi.org/pypi/mario-addons


.. end-badges

More commands for Mario.

* Free software: MIT license

Installation
============

::

    pip install mario-addons

Documentation
=============


https://mario-addons.readthedocs.io/


Development
===========

To run the all tests run::

    tox

Note, to combine the coverage data from all the tox environments run:

.. list-table::
    :widths: 10 90
    :stub-columns: 1

    - - Windows
      - ::

            set PYTEST_ADDOPTS=--cov-append
            tox

    - - Other
      - ::

            PYTEST_ADDOPTS=--cov-append tox
