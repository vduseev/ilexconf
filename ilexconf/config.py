from ilexconf.helpers import keyval_to_dict

from typing import Any, Dict, Mapping, List, Sequence


# [not-sequence-types]
# These python types are not considered to be Sequences in ilexconf,
# even though, technically, they are Sequences in Python.
NOT_SEQUENCE_TYPES = (str, bytes, bytearray)
# [not-sequence-types]


class Config(dict):
    """Config is a dictionary compatible object.

    **Why Config?** Config provides *convenient* methods to work with mappings. It allows 
    addressing the keys via attributes and correctly merges multiple mappings
    within one object.

    **Goal.** The main purpose of the Config is to simplify the process of working
    with multiple mappings by combining them within one object and adding
    convenience methods to access values, create them, change them, or dump
    them to files.
    
    **How it works.** Config inherits ``dict`` class, but behaves like a ``defaultdict``. When
    a key that does not exist in the Config is accessed then an empty Config
    value is created in its place. Config overrides ``dict`` methods to implement
    its convenient flow.

    Args:
        *mappings (Mapping): Mapping-like objects that will be used to
            initialize Config object.
        **kwargs: Keyword arguments that will be used to initialize Config
            object. If the key contains ``__`` separator in its name then
            the key will be split by it to form a hierarchical dictionary with
            the value in it.

    Examples:
        Create empty Config object:

        >>> config = Config()
        Config{}

        Create Config from dictionary:

        >>> config = Config({ "name": "Boris" })
        Config{'name': 'Boris'}

        Create Config from keyword arguments:

        >>> config = Config(database__host = "172.31.49.120")
        Config{'database': Config{'host': '172.31.49.120'}}

        
    """

    def __init__(self, *mappings: Mapping[Any, Any], **kwargs: Dict):
        super().__init__()

        # Merge in values of mappings
        self.merge(*mappings, **kwargs)

    def __getitem__(self, item):
        if isinstance(item, str) and "." in item:
            key, subkey = item.split(".", maxsplit=1)
            return self._dd_getitem(key).__getitem__(subkey)
        else:
            return self._dd_getitem(item)

    def __getattr__(self, attr):
        return self._dd_getitem(attr)

    def __setitem__(self, item, value):
        value = self.parse(value)
        if isinstance(item, str) and "." in item:
            key, subkey = item.split(".", maxsplit=1)
            self._dd_getitem(key).__setitem__(subkey, value)
        else:
            dict.__setitem__(self, item, value)

    def __setattr__(self, attr, value):
        value = self.parse(value)
        dict.__setitem__(self, attr, value)

    def __repr__(self):
        return f"Config{dict.__repr__(self)}"

    def merge(self, *mappings: Mapping[Any, Any], **kwargs) -> None:
        """Merge values of mappings with current config recursively."""

        # For every key of that mapping
        for mapping in mappings:
            for key, value in mapping.items():

                parsed = self.parse(value)
                self.update(
                    {
                        key: Config(self[key], parsed)
                        if key in self
                        and isinstance(self[key], Config)
                        and isinstance(parsed, Config)
                        else parsed
                    }
                )

        # Merge in values of keyword arguments
        for k, v in kwargs.items():
            keyval_dict = keyval_to_dict(k, v)
            self.merge(keyval_dict)

    @staticmethod
    def parse(value: Any):
        # If value is another Mapping: dict, Config, etc.
        if isinstance(value, Mapping):
            return Config(value)

        # If value is a Sequence but not str, bytes, or bytearray
        elif isinstance(value, Sequence) and not isinstance(value, NOT_SEQUENCE_TYPES):
            l = list()
            for i in value:
                l.append(Config.parse(i))
            # Return sequence with the same type
            t = type(value)
            return t(l)

        # If value is anything else
        else:
            return value

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
        return Config(d)

    def lower(self):
        """Lowercase all string keys of the configuration"""

        return Config(self.as_dict(lowercase=True))

    def upper(self):
        """Uppercase all string keys of the configuration"""

        return Config(self.as_dict(uppercase=True))

    def copy(self):
        """Return deep copy of the Config object."""

        return Config(self.as_dict())

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

    def _dd_getitem(self, item):
        """Implements defaultdict feature

        DefaultDict getitem method
        """
        if item not in self:
            dict.__setitem__(self, item, Config())
        return dict.__getitem__(self, item)
