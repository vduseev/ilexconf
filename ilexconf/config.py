from collections import defaultdict
from typing import (
    Any,
    Dict,
    Mapping,
)


class Config(defaultdict):
    """
    Config is a dictionary of other configs forming hierarchical structure.

    The Config takes any number of mappings as an input and merges them.
    It can be initialized as an empty dictionary as well.

        ```
        from hollysettings import Config
        foo = Config()
        bar = Config({ "a": { "b" : 2 }}, foo)
        ```

    Config is intented to be initialized by the settings read from files,
    command line arguments, environment variables, default variables, etc.

    After Config is created you can perform all usual dictionary operations
    on it. However, you can also:

        - Serialize it, dump it to json, and write to file

            ```
            from hollysettings import Config, to_json
            cfg = Config({"a": 1})
            to_json(cfg, "settings.json")
            ```

        - Convert it to standard Python dict object
          (see `as_dict` method).

        - Flatten it, i.e. transform hierarchical nature of config to flat
          one-level dictionary with dottet keys like "my.key"
          (see `flatten` method).

        - Read and write any key using any of the following methods:

            As in Python dictionary:
              `config["my"]["key"]`

            As if it was flat dictionary:
              `config["my.key"]`

            As if it was object with attributes:
              `config.my.key`

        - Covert it to hierarchical table and print it
          (see `as_table` method).

        - Make deep copy of it
          (see `copy` method).
    """

    def __init__(
        self,
        *mappings: Mapping[str, Any],
    ):
        """
        Constructor.
        """

        # Initialize super class as defaultdict with None value for
        # nonexisting keys, so that None is returned instead of throwing
        # KeyError exection.
        super().__init__(*(lambda: Config(),))

        # Merge values of mappings
        for m in mappings:
            for key in m.keys():
                if isinstance(m[key], Mapping):
                    if key in self:
                        self.update({key: Config(self[key], m[key])})
                    else:
                        self.update({key: Config(m[key])})
                else:
                    self.update({key: m[key]})

    def __getitem__(self, item):
        if isinstance(item, str) and "." in item:
            key, subkey = item.split(".", maxsplit=1)
            return dict.__getitem__(self, key).__getitem__(subkey)
        else:
            return dict.__getitem__(self, item)

    def __getattr__(self, attr):
        return dict.__getitem__(self, attr)

    def __setitem__(self, item, value):
        if isinstance(item, str) and "." in item:
            key, subkey = item.split(".", maxsplit=1)
            dict.__getitem__(self, key).__setitem__(subkey, value)
        else:
            dict.__setitem__(self, item, value)

    def __setattr__(self, attr, value):
        dict.__setitem__(self, attr, value)

    def as_dict(self):
        d = dict()
        for key in self.keys():
            if isinstance(self[key], Config):
                d[key] = self[key].as_dict()
            else:
                d[key] = self[key]
        return d

    def as_table(self):
        pass
