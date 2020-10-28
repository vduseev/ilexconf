from typing import Any, Dict, Hashable, Mapping, List, Sequence, Union


# [not-sequence-types]
# These python types are not considered to be Sequences in ilexconf,
# even though, technically, they are Sequences in Python.
NOT_SEQUENCE_TYPES = (str, bytes, bytearray)
# [not-sequence-types]


class Config(dict):
    def __init__(self, *mappings: Mapping[Hashable, Any], **kwargs: Dict):
        super().__init__()
        self.merge(*mappings, **kwargs)

    def __getitem__(self, item):
        if isinstance(item, str) and "." in item:
            key, subkey = item.split(".", maxsplit=1)
            return self._default_getitem(key).__getitem__(subkey)
        else:
            return self._default_getitem(item)

    def __getattr__(self, attr):
        return self._default_getitem(attr)

    def __setitem__(self, item, value):
        value = self._parse_value(value)
        if isinstance(item, str) and "." in item:
            key, subkey = item.split(".", maxsplit=1)
            self._default_getitem(key).__setitem__(subkey, value)
        else:
            dict.__setitem__(self, item, value)

    def __setattr__(self, attr, value):
        value = self._parse_value(value)
        dict.__setitem__(self, attr, value)

    def __repr__(self):
        return f"Config{dict.__repr__(self)}"

    def merge(self, *mappings: Mapping[Hashable, Any], _strategy="recursive", _separator="__", _inverse=False, **kwargs) -> "Config":
        # Collect all key-value pairs from mappings and keyword arguments
        # into a single ordered list with last element having the highest
        # priority.
        items = []
        # From mappings
        for mapping in mappings:
            items += mapping.items()
        # From keyword arguments
        items += kwargs.items()

        for k, v in items:
            parsed = Config.from_keyvalue(k, v, separator=_separator)
            if _inverse:
                parsed.update(self, strategy=_strategy)
                super().__init__()
                self.merge(parsed, _strategy=_strategy, _separator=_separator, _inverse=False)
            else:
                self.update(parsed, strategy=_strategy)

        return self
    
    def submerge(self, *mappings: Mapping[Hashable, Any], _strategy="recursive", _separator=".", **kwargs) -> "Config":
        return self.merge(*mappings, _strategy=_strategy, _separator=_separator, _inverse=True, **kwargs)

    def update(self, config: "Config", strategy="recursive") -> "Config":
        if not isinstance(config, Config):
            raise TypeError(f"Unsupported type of config argument: {type(config)}. Only Config is supported.")
       
        for key in config:
            if strategy == "recursive" and key in self and isinstance(self[key], Config) and isinstance(config[key], Config):
                self[key].update(config[key], strategy=strategy)
            else:
                self[key] = config[key]

        return self

    @staticmethod
    def from_keyvalue(key: Hashable, value: Any, prefix: str = "", separator: str = "__", lowercase: bool = False, uppercase: bool = False) -> "Config":
        parts = Config._parse_key(key, prefix=prefix, separator=separator, lowercase=lowercase, uppercase=uppercase)
        if not parts:
            return Config()

        value = Config._parse_value(value)

        # Fill in a hierarchical structure by
        # continuously building up the config in reverse order.
        result = value
        while parts:

            # Take the last part of the key no processed yet
            k = parts.pop()

            # Create an empty config and assign current saved ``result``
            # to ``k`` in it.
            config = Config()
            config[k] = result

            # Rebind result to point to the newly created config
            result = config

        return result

    def flatten(self, prefix="", separator="."):
        """Flatten current config so that there is no hierarchy."""

        d = dict()
        p = f"{prefix}{separator}" if prefix else ""
        for key in self.keys():
            if isinstance(self[key], Config):
                flattened = self[key].flatten(prefix=f"{p}{key}", separator=separator)
                d.update(flattened)
            else:
                d[f"{p}{key}"] = self[key]
        return d

    def lower(self):
        """Lowercase all string keys of the configuration"""

        return Config(self.as_dict(lowercase=True))

    def upper(self):
        """Uppercase all string keys of the configuration"""

        return Config(self.as_dict(uppercase=True))

    def copy(self):
        """Return deep copy of the Config object."""

        config = Config._parse_value(self)
        return config
        # return Config(self.as_dict())

    def as_dict(self, lowercase: bool = False, uppercase: bool = False):
        """Convert configuration to dict object.

        `lowercase` takes precedence over `uppercase`.
        """

        d = dict()
        for key in self.keys():
            assignment_key = (
                key.lower()
                if lowercase and isinstance(key, str)
                else key.upper()
                if uppercase and isinstance(key, str)
                else key
            )
            if isinstance(self[key], Config):
                d[assignment_key] = self[key].as_dict(
                    lowercase=lowercase, uppercase=uppercase
                )
            else:
                d[assignment_key] = self[key]
        return d

    def as_table(
        self,
        headers: List[str] = ["Key", "Value"],
        indentation: str = "  ",
        limit: int = 0,
    ):
        """Transform configuration into table structure.

        Returns tuple of headers and rows.
        Returned structure is suitable for printing by Cleo library.
        """

        def processor(c: Dict, rows: List, level: int):
            # Increment level so that all child rows are indented
            level += 1
            for k in sorted(c.keys()):
                key = k
                table_key = f"{indentation * level}{key}"

                # Try to interpret the field as a dictionary
                try:
                    # Can't do isinstance(c, collections.Mapping) because
                    # config that needs this method is not a Mapping subclass
                    is_dict = hasattr(c[k], "keys")
                except KeyError:  # pragma: no cover
                    is_dict = False

                if limit and len(rows) >= limit:
                    break

                if is_dict:
                    # Add category row
                    rows.append([table_key, ""])
                    # Recursive call
                    processor(c[k], rows, level)

                else:
                    # Transform multiline strings into singleline
                    singleline = " ".join(
                        str(c[k]).replace("\n", " ").replace("\t", " ").split()
                    )

                    # Clip long string by character limit to fit onto the screen
                    clipped = (
                        singleline if len(singleline) < 80 else f"{singleline[:76]} ..."
                    )
                    rows.append([table_key, clipped])

        # Populate rows
        rows = []
        processor(self, rows, -1)
        if limit and len(rows) >= limit:
            rows.append(["...", "..."])

        return (headers, rows)

    def _default_getitem(self, item):
        """Implements defaultdict feature

        DefaultDict getitem method
        """
        if item not in self:
            dict.__setitem__(self, item, Config())
        return dict.__getitem__(self, item)

    @staticmethod
    def _parse_key(key: Hashable, prefix: str = "", separator: str = "__", lowercase: bool = False, uppercase: bool = False) -> List[Hashable]:
        if not isinstance(key, str):
            # When key is not a string, then it cannot be split.
            # Thus, return the key as is
            return [key]

        if prefix and not key.startswith(prefix):
            # If prefix is specified, then return nothing
            return []

        # Strip key off of prefix
        key = key[len(prefix) :]

        # Convert to lowercase/uppercase if needed
        key, prefix, separator = [
            v.lower() if lowercase else v.upper() if uppercase else v for v in [
                key, prefix, separator
            ]
        ]

        # Strip any dangling separator leftovers around the key
        if separator and key.startswith(separator):
            key = key[len(separator) :]
        if separator and key.endswith(separator):
            key = key[: -len(separator)]

        # Split the key into 2 parts using the separator.
        # If the key does not contain a separator string in it, then just return a parts
        # list consisting of the key itself.
        parts = key.split(separator, maxsplit=1) if separator else [key]

        if len(parts) > 1:
            # When key has been split successfully, then the second part of the split
            # is eligible for the same processing routine and a recursive call is made.
            key, subkey = parts  # unpack split parts for readability
            return [key] + Config._parse_key(subkey, prefix="", separator=separator, lowercase=lowercase, uppercase=uppercase)

        else:
            # If key was not split, then there is nothing to split anymore and we just
            # return the key
            return [parts[0]]

    @staticmethod
    def _parse_value(value: Any) -> Union["Config", Sequence, Any]:
        # If value is another Mapping: dict, Config, etc.
        if isinstance(value, Mapping):
            return Config(value)

        # If value is a Sequence but not str, bytes, or bytearray
        elif isinstance(value, Sequence) and not isinstance(value, NOT_SEQUENCE_TYPES):
            l = list()
            for i in value:
                l.append(Config._parse_value(i))
            # Return sequence with the same type
            t = type(value)
            return t(l)

        # If value is anything else
        else:
            return value
