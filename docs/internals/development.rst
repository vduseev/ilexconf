===========
Development
===========

Cloning
=======

.. code-block:: bash

   git clone git@github.com:ilexconf/ilexconf.git

Building
========

.. code-block:: bash

   poetry install -E yaml -E console

Testing
=======

.. code-block:: bash

   poetry run pytest --cov

Building documentation
======================

Full documentation is hosted at:

* `ilexconf.com <https://ilexconf.com>`_; and
* `ilexconf.readthedocs.io <https://ilexconf.readthedocs.io>`_.

Process:

* Documentation is written using `reStructuredText` and uses real code snippets from the unit tests and source code.
* Documentation is built with `Sphinx <https://www.sphinx-doc.org/>`_ using `sphinx-material <https://github.com/bashtage/sphinx-material>`_ theme.
* For Github Pages documentation is built using Github Actions.
* Read the Docs builds their version automatically based on the `.readthedocs.yml` config in the project root directory.

Building:

.. code-block:: bash

   make -C docs html

Then open the ``index.html`` file in the ``docs/_build`` directory in your browser.
