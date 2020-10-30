========
Adapters
========

Common interface
================

All adapters share the same interface and form. For each supported format is a ``from_<format>`` 
function to read and parse the format from source and a ``to_<format>`` function to write the
config in that format to file or to string. 

.. toctree::
   :caption: List of supported adapters
   :titlesonly:

   json <_adapters/json>
   yaml <_adapters/yaml>
   ini <_adapters/ini>