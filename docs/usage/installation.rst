============
Installation
============

pip
===

Install using ``pip``:

.. code:: bash

   pip install ilexconf

This will install:

-  Pure Python library without any dependencies
-  Support for 

   -  ``JSON``
   -  ``INI``
   -  environment variables
   -  ``argparse`` parsing results

-  ``ilexconf`` command line executable that does nothing

Command line
------------

.. code:: bash

   pip install ilexconf[console]

This will install:

-  *All of the above*
-  ``Cleo`` based rich :ref:`command line application`.
-  Enables ``CommandConfig`` class that you can include into your Cleo application.

YAML, TOML, etc
---------------

.. code:: bash

   pip install ilexconf[yaml]

This will install:

-  Support for YAML adapters such as ``from_yaml`` and ``to_yaml``.

poetry
======

Install using ``poetry``:

.. code:: bash

   poetry add ilexconf

Install with extras:

.. code:: bash

   poetry add ilexconf -E console -E yaml

This will install:

-  ``ilexconf`` main library
-  Support for YAML configs
-  Command line application named ``ilexconf``.

Poetry automatically creates a virtual environment when you use it. It will install ``ilexconf``
in this venv and will make the CLI available in it as well as install required adapters, such
as YAML.
