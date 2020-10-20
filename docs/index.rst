.. image:: _static/github-logo.png
   :alt: ilexconf logo

.. raw:: html

   <p align="center">
   <a href="https://travis-ci.org/ilexconf/ilexconf"><img alt="Build status of package" src="https://img.shields.io/travis/ilexconf/ilexconf?logo=travis"></a>
   <a href="https://github.com/ilexconf/ilexconf/actions?query=workflow%3Adocs"><img alt="Build status of GitHub pages docs" src="https://img.shields.io/github/workflow/status/ilexconf/ilexconf/docs?label=docs&logo=github"></a>
   <a href="https://ilexconf.readthedocs.io/"><img alt="Build status of Read the Docs" src="https://img.shields.io/readthedocs/ilexconf?label=readthedocs&logo=read-the-docs"></a>
   <a href="https://codecov.io/gh/ilexconf/ilexconf"><img alt="Code coverage report" src="https://img.shields.io/codecov/c/github/ilexconf/ilexconf?logo=codecov"></a>
   <a href="https://pypi.org/project/ilexconf/"><img alt="PyPI" src="https://img.shields.io/pypi/v/ilexconf?logo=pypi&color=blue"></a>
   </p>

Ilexconf Documentation
======================

``ilexconf`` is a Python library to load and merge configs from multiple sources,
access & change the values, and write them back. It has no dependencies
by default but provides additional functions, relying on popular libraries 
to parse `yaml`, `toml`, provide command line app, etc.

Features
--------

* Assign to non-existent keys
* Correctly merges lists

Table of Contents
-----------------

.. toctree::
   :caption: Usage
   :maxdepth: 1

   usage/installation
   usage/quickstart


.. toctree::
   :caption: Internals
   :maxdepth: 1

   internals/development
   internals/implementation

