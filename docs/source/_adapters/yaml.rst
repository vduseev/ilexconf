====
YAML
====

YAML adapters ``from_yaml`` and ``to_yaml`` allow reading and writing YAML files or strings.

Dependencies
============

In order to support YAML adapters ``pyyaml`` or ``ruamel.yaml`` libraries must be installed
in your python environment. Alternatively, install ``ilexconf`` with extras:

.. code:: bash

   pip install ilexconf[yaml]


from_yaml
=========

.. autofunction:: ilexconf.adapters.yaml.from_yaml

to_yaml
=======

.. autofunction:: ilexconf.adapters.yaml.to_yaml
