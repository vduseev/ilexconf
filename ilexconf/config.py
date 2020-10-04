from collections import defaultdict

from ilexconf.helpers import keyval_to_dict

from typing import Any, Dict, Mapping, List, Sequence

# TODO: Implement from_json, from_env, etc.
# TODO: ? merging mappings with dotted keys
# TODO: Super weird error when item did not exist and we created it
# TODO: CLI
# TODO: Proper typing
# TODO: Proper coverage


class Config(defaultdict):
    """
    Config is a dictionary of other configs forming hierarchical structure.
    """

    def __init__(self, *mappings: Mapping[Any, Any], **kwargs: Dict):
        """
        Constructor.
        """

        # Initialize super class as defaultdict with None value for
        # nonexisting keys, so that None is returned instead of throwing
        # KeyError exection.
        super().__init__(*(lambda: Config(),))

        # Merge in values of mappings
        for m in mappings:
            self.merge(m)

        # Merge in values of keyword arguments
        for k, v in kwargs.items():
            parsed = keyval_to_dict(k, v)
            self.merge(parsed)

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

    def __repr__(self):
        # d = dict()
        # for key in self.keys():
        #     if isinstance(self[key], Config):
        #         d[key] = self[key].__repr__()
        #     else:
        #         d[key] = str(self[key])
        return f"Config{dict.__repr__(self)}"

    def merge(self, mapping: Mapping[Any, Any]) -> None:
        """
        Merge values of mapping with current config recursively.
        """
        # For every key of that mapping
        for key, value in mapping.items():

            parsed = self._parse(value)
            self.update(
                {
                    key: Config(self[key], parsed)
                    if key in self and isinstance(self[key], Config)
                    else parsed
                }
            )

    def _parse(self, value: Any):
        # If value is another Mapping: dict, Config, etc.
        if isinstance(value, Mapping):
            return Config(value)

        # If value is a Sequence but not str, bytes, or bytearray
        elif isinstance(value, Sequence) and not isinstance(
            value, (str, bytes, bytearray)
        ):
            l = list()
            for i in value:
                l.append(self._parse(i))
            # Return sequence with the same type
            t = type(value)
            return t(l)

        # If value is anything else
        else:
            return value

    def flatten(self, prefix="", separator="."):
        """
        Flatten Config object to dictionary with depth 1.
        """
        d = dict()
        p = f"{prefix}{separator}" if prefix else ""
        for key in self.keys():
            if isinstance(self[key], Config):
                flattened = self[key].flatten(prefix=f"{p}{key}", separator=separator)
                d.update(flattened)
            else:
                d[f"{p}{key}"] = self[key]

    def copy(self):
        """
        Return deep copy of the Config object.
        """
        return Config(self.as_dict())

    def as_dict(self):
        d = dict()
        for key in self.keys():
            if isinstance(self[key], Config):
                d[key] = self[key].as_dict()
            else:
                d[key] = self[key]
        return d

    def as_table(
        self,
        headers: List[str] = ["Setting", "Value"],
        indentation: str = "  ",
        limit: int = 0,
    ):
        """
        Transform multilevel dictionary into table structure suitable for printing by Cleo library.
        """

        def processor(c: Dict, rows: Rows, level: int):
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
                except KeyError:
                    is_dict = False

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

                if limit > 0 and len(rows) > limit:
                    break

        # Populate rows
        rows = []
        processor(self, rows, -1)
        if len(rows) > limit:
            rows.append(["...", "..."])

        return (headers, rows)
