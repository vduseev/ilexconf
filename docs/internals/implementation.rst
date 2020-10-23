=========
Internals
=========

Implementation
==============

Design
------

Most of developers have encountered the problem of having their configs in multiple 
places (for user's convenience), including files (in several places), environment variables,
command line arguments, some default values, some external sources, etc.

**How do we merge and work with all of those?** Well, we'd have to implement some kind 
of a "Configuration" class that does all that. It would read the files, parse them properly,
parse command line args, parse environment variables, somehow merge it all with proper
priorities and build some kind of a dictionary out of it all to work with the configuration
in our program.

That sounds fine but do we really have to do it **every time**? And can't the resulting config
be more friendly, more accessible, verifiable, convenient to use?

That's how the search for Python library that does that started. Unfortunately none of the
existing solution were able to do it all. Or at least accomplish the most significant aspects
of convenient usage.

.. note:: ``ilexconf`` heavily borrows its ideas from `python-configuration <https://github.com/tr11/python-configuration>`_ library.

Being a dictionary
------------------

Under the hood ``ilexconf`` is implemented as subclass of ``dict``. 

It mostly behaves just like a ``dict``. For example, it inherits the ``.clear()`` method from *dict*.
Some aspects, however, are not that familiar. For instance, you can assign a value to a key that does
not exist yet, and the key will be created and assigned a value (even if it's a nested key).

Every value in the ``Config`` instance can be a 

* ``Mapping``, represented as another ``Config`` object
* ``Sequence`` (with some exceptions below)
* other types, such as ``int``, ``float``, ``str``, etc.

This creates a hierarchy of ``Config`` and plain objects.

.. note:: 

   .. literalinclude:: ../../ilexconf/config.py
      :language: python
      :start-after: [not-sequence-types]
      :end-before: [not-sequence-types]

Overridden methods
------------------

Some ``dict`` methods are overloaded with custom logic to support convenient get/set
approach presented by the library.
The essence of the library is in this overridden methods of ``dict`` class.

``__getitem__``

.. literalinclude:: ../../ilexconf/config.py
   :pyobject: Config.__getitem__


``__getattr__``

.. literalinclude:: ../../ilexconf/config.py
   :pyobject: Config.__getattr__


``__setitem__``

.. literalinclude:: ../../ilexconf/config.py
   :pyobject: Config.__setitem__


``__setattr__``

.. literalinclude:: ../../ilexconf/config.py
   :pyobject: Config.__setattr__

They rely on the ``_dd_getitem`` method that implements the ``defaultdict`` functionality 
without actually subclassing it (see `Issue #6 <https://github.com/ilexconf/ilexconf/issues/6>`_ to understand why such approach was taken). 

``_dd_getitem``

.. literalinclude:: ../../ilexconf/config.py
   :pyobject: Config._dd_getitem
