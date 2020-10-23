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

-  Create empty config

   .. literalinclude:: ../ilexconf/tests/test_index.py
      :language: python
      :lines: 5-6
      :dedent: 4

-  Assign to non-existent keys 

   .. literalinclude:: ../ilexconf/tests/test_index.py
      :language: python
      :lines: 8
      :dedent: 4

-  Access values however you want

   .. literalinclude:: ../ilexconf/tests/test_index.py
      :language: python
      :lines: 11,14,17,20,23,26
      :dedent: 8

-  Correctly merge lists

   .. literalinclude:: ../ilexconf/tests/test_index.py
      :language: python
      :lines: 30-33,36,39,42
      :dedent: 8

-  Support ``json``, ``ini``, ``yaml``, ``toml``, ``python modules``

   .. code:: python

      config = from_json("settings.json")
      config = from_python("settings.py")

-  Correctly merge configs 

-  Support environment variables

-  Support command line arguments as configuration 

-  Rich :ref:`command line application`

   .. code:: shell

      # Show config variables
      ilexconf list config.json 

      # Set variable
      ilexconf set my_config.json my.key my_value

.. note:: Every single example on this page is `unit tested <https://github.com/ilexconf/ilexconf/blob/master/ilexconf/tests/test_index.py>`_.

Table of Contents
-----------------

.. toctree::
   :caption: Quick Start
   :titlesonly:

   usage/quickstart

.. toctree::
   :caption: Installation
   :titlesonly:

   usage/installation

.. toctree::
   :caption: Usage
   :titlesonly:

   usage/commandline


.. toctree::
   :caption: Internals
   :titlesonly:

   internals/development
   internals/implementation

