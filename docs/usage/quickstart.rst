===========
Quick start
===========

The steps below describe how to create, modify, save, merge, subclass Configs and much more.
Similarly to many other parts of this documentation Quick Start section is generated out of actual unit tests that cover the functionality described below.

Create config
=============

Config objects are initialized using arbitrary number of mappings and keyword arguments.
Any ``config`` object can be populated by assigning values directly or by merging another config into it. 
Values can assigned to the keys that do not exist yet. 

``merge`` method is almost identical to the ``Config()`` constructor. Actually, ``Config()`` just uses ``merge`` inside itself.
The only difference is that the constructor, obviously, creates new object, while ``merge`` is merging values into an existing one.

.. literalinclude:: ../../ilexconf/tests/test_quick_start.py
   :language: python
   :start-after: [create]
   :end-before: [create]

When we initialize config all the values are merged. Arguments are merged in order they are provided.
Every next argument is merged on top of the previous mapping values.
And keyword arguments override even that. *For more details read about merging below*.

Read configs from different sources
===================================

Files like `.json`, `.yaml`, `.toml`, `.ini`, `.env`, `.py` as well as environment variables can all be read & loaded using a set of `from_` functions.

.. literalinclude:: ../../ilexconf/tests/test_quick_start.py
   :language: python
   :start-after: [read]
   :end-before: [read]

Access values
=============

You can access any key in the hierarchical structure using classical Python dict notation, dotted keys, attributes, or any combination of this methods.

.. literalinclude:: ../../ilexconf/tests/test_quick_start.py
   :language: python
   :start-after: [access]
   :end-before: [access]

Upsert values (update or insert)
================================

Similarly, you can set values of any key (*even if it doesn't exist in the Config*) using all of the ways above.

**Notice**, *contrary to what you would expect from the Python dictionaries, setting nested keys that do not exist is **allowed***.

.. literalinclude:: ../../ilexconf/tests/test_quick_start.py
   :language: python
   :start-after: [upsert]
   :end-before: [upsert]

Merging values
==============

If you just assign a value to any key, you override any previous value of that key.
In order to merge assigned value with an existing one, use `merge` method.

.. literalinclude:: ../../ilexconf/tests/test_quick_start.py
   :language: python
   :start-after: [merge]
   :end-before: [merge]

`merge` respects the contents of each value. For example, merging two dictionaries with the same key would not override that key completely. Instead, it will recursively look into each key and try to merge the contents. Take this example:

.. literalinclude:: ../../ilexconf/tests/test_quick_start.py
   :language: python
   :start-after: [smart-merge]
   :end-before: [smart-merge]

Convert to dict
===============

For any purposes you might find fit you can convert entire structure of the Config object into dictionary, which will be essentially returned to you as a deep copy of the object.

.. literalinclude:: ../../ilexconf/tests/test_quick_start.py
   :language: python
   :start-after: [as-dict]
   :end-before: [as-dict]

Save config to file
===================

You can serialize the file as ``json``, ``toml``, ``ini`` or other types any time using a set of ``to_`` functions.

.. literalinclude:: ../../ilexconf/tests/test_quick_start.py
   :language: python
   :start-after: [write]
   :end-before: [write]

Subclass and add your own logic
===============================

Subclassing ``Config`` class is very convenient for implementation of your own config classes with custom logic.
Consider this example:

.. literalinclude:: ../../ilexconf/tests/test_quick_start.py
   :language: python
   :start-after: [subclass]
   :end-before: [subclass]

Here is what will get generated when we instantiate this custom ``MyConfig`` object.

.. literalinclude:: ../../ilexconf/tests/test_quick_start.py
   :language: python
   :start-after: [test-subclass]
   :end-before: [test-subclass]
