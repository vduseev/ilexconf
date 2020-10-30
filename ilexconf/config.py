from typing import (
    Any,
    Dict,
    Hashable,
    Mapping,
    List,
    Sequence,
    Union,
    Callable,
    Tuple,
)


# [not-sequence-types]
# These python types are not considered to be Sequences in ilexconf,
# even though, technically, they are Sequences in Python.
STR_TYPES = (str, bytes, bytearray)
# [not-sequence-types]


class BaseConfig(dict):
    pass


class Config(BaseConfig):
    def __init__(self, *mappings: Mapping[Hashable, Any], **kwargs: Dict):
        super().__init__()
        self.merge(*mappings, **kwargs)

    def get(
        self, key: Hashable, sep: str = ".", default: Any = BaseConfig()
    ) -> Any:
        if key in self:
            return dict.__getitem__(self, key)
        if isinstance(key, str) and sep and sep in key:
            key, subkey = key.split(sep, maxsplit=1)
            return self._default_getitem(key, default).get(
                subkey, sep=sep, default=default
            )
        else:
            return self._default_getitem(key, default)

    def set(
        self,
        key: Hashable,
        value: Any,
        method: str = "recursive",
        sep: str = ".",
        inverse: bool = False,
    ) -> Any:
        parsed = Config.from_keyvalue(key, value, sep=sep)

        if inverse:
            parsed.update(self, method=method)
            self.clear()

        self.update(parsed, method=method)

        return self

    def merge(
        self,
        *mappings: Mapping[Hashable, Any],
        _method: str = "recursive",
        _sep: str = "__",
        _inverse: bool = False,
        **kwargs,
    ) -> "Config":
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
            self.set(k, v, method=_method, sep=_sep, inverse=_inverse)

        return self

    def submerge(
        self,
        *mappings: Mapping[Hashable, Any],
        _method: str = "recursive",
        _sep: str = "__",
        **kwargs,
    ) -> "Config":
        return self.merge(
            *mappings,
            _method=_method,
            _sep=_sep,
            _inverse=True,
            **kwargs,
        )

    def update(self, config: "Config", method: str = "recursive") -> "Config":
        if not isinstance(config, Config):
            raise TypeError((
                "Unsupported type of config argument: "
                f"{type(config)}. Only Config is supported."
            ))

        for key in config:
            if (
                method == "recursive"
                and key in self
                and isinstance(dict.__getitem__(self, key), Config)
                and isinstance(dict.__getitem__(config, key), Config)
            ):
                dict.__getitem__(self, key).update(
                    dict.__getitem__(config, key), method=method
                )
            else:
                dict.__setitem__(self, key, dict.__getitem__(config, key))

        return self

    @staticmethod
    def from_keyvalue(
        key: Hashable,
        value: Any,
        prefix: str = "",
        sep: str = "__",
        lowercase: bool = False,
        uppercase: bool = False,
    ) -> "Config":
        parts = Config.parse_key(
            key,
            prefix=prefix,
            sep=sep,
            lowercase=lowercase,
            uppercase=uppercase,
        )
        if not parts:
            return Config()

        # value = Config.parse_value(value)
        value = Config.traverse(value)

        # Fill in a hierarchical structure by
        # continuously building up the config in reverse order.
        result = value
        while parts:

            # Take the last part of the key no processed yet
            k = parts.pop()

            # Create an empty config and assign current saved ``result``
            # to ``k`` in it.
            config = Config()
            dict.__setitem__(config, k, result)
            # config = Config().set(k, result)
            # config[k] = result

            # Rebind result to point to the newly created config
            result = config

        return result

    @staticmethod
    def parse_key(
        key: Hashable,
        prefix: str = "",
        sep: str = "__",
        lowercase: bool = False,
        uppercase: bool = False,
    ) -> List[Hashable]:
        if not isinstance(key, str):
            # When key is not a string, then it cannot be split.
            # Thus, return the key as is
            return [key]

        if not isinstance(prefix, str):
            prefix = str(prefix)

        if prefix and not key.startswith(prefix):
            # If prefix is specified, then return nothing
            return []

        # Strip key off of prefix
        key = key[len(prefix) :]

        # Convert to lowercase/uppercase if needed
        key, prefix, sep = [
            v.lower() if lowercase else v.upper() if uppercase else v
            for v in [key, prefix, sep]
        ]

        # Strip any dangling separator leftovers around the key
        if sep and key.startswith(sep):
            key = key[len(sep) :]
        if sep and key.endswith(sep):
            key = key[: -len(sep)]

        # Split the key into 2 parts using the separator.
        # If the key does not contain a separator string in it, then just return a parts
        # list consisting of the key itself.
        parts = key.split(sep, maxsplit=1) if sep else [key]

        if len(parts) > 1:
            # When key has been split successfully, then the second part of the split
            # is eligible for the same processing routine and a recursive call is made.
            key, subkey = parts  # unpack split parts for readability
            return [key] + Config.parse_key(
                subkey,
                prefix="",
                sep=sep,
                lowercase=lowercase,
                uppercase=uppercase,
            )

        else:
            # If key was not split, then there is nothing to split anymore and we just
            # return the key
            return [parts[0]]

    @staticmethod
    def traverse(
        arg: Any,
        func=lambda k, v, **kwargs: (k, v),
        key_order=lambda k: k,
        list_order=lambda l: l,
        **kwargs,
    ) -> Any:
        if "_depth" not in kwargs:
            kwargs["_depth"] = 0
        kwargs["_depth"] += 1

        if isinstance(arg, Mapping):
            config = Config()
            keys = key_order(arg.keys())
            for k in keys:
                v = arg[k]
                k, v = func(k, v, **kwargs)
                v = Config.traverse(
                    v,
                    func,
                    key_order=key_order,
                    list_order=list_order,
                    **kwargs,
                )
                dict.__setitem__(config, k, v)

            return config

        # If value is a Sequence but not str, bytes, or bytearray
        elif isinstance(arg, Sequence) and not isinstance(arg, STR_TYPES):
            l = list()
            items = list_order(arg)
            for i in items:
                _, v = func(None, i, **kwargs)
                v = Config.traverse(v, func, **kwargs)
                l.append(v)

            # Return sequence of the same type
            t = type(arg)
            return t(l)

        # If value is anything else
        else:
            _, v = func(None, arg, **kwargs)
            return v

    def flatten(self, prefix: str = "", sep: str = "."):
        """Flatten current config so that there is no hierarchy."""

        d = dict()
        p = f"{prefix}{sep}" if prefix else ""
        for key in self:
            if isinstance(self.get(key), Config):
                flattened = self.get(key).flatten(prefix=f"{p}{key}", sep=sep)
                d.update(flattened)
            else:
                d[f"{p}{key}"] = self.get(key)
        return d

    def map(
        self,
        func: Callable[
            [Hashable, Any], Tuple[Hashable, Any]
        ] = lambda k, v, **kwargs: (k, v),
        inplace: bool = False,
        **kwargs,
    ):
        config = Config.traverse(self, func, **kwargs)

        if inplace:
            self.clear()
            self.update(config)
            config = self

        return config

    def lower(self, inplace=False):
        """Lowercase all string keys of the configuration"""
        return self.map(
            func=lambda k, v, **kwargs: (
                k.lower() if isinstance(k, str) else k,
                v,
            ),
            inplace=inplace,
        )

    def upper(self, inplace=False):
        """Uppercase all string keys of the configuration"""
        return self.map(
            func=lambda k, v, **kwargs: (
                k.upper() if isinstance(k, str) else k,
                v,
            ),
            inplace=inplace,
        )

    def copy(self):
        """Return deep copy of the Config object."""
        return self.map(inplace=False)

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

        def do_me(k, v, rows, _depth, limit):
            if k is None:
                return k, v

            table_key = "  " * (_depth - 1) + k

            if not limit or limit and len(rows) < limit:
                value = ""
                if not isinstance(v, Config):
                    s = " ".join(
                        str(v).replace("\n", " ").replace("\t", " ").split()
                    )
                    value = s if len(s) < 80 else f"{s[:76]}..."
                rows.append([table_key, value])

            return k, v

        rows = []
        Config.traverse(
            self,
            func=do_me,
            key_order=lambda keys: sorted(keys),
            rows=rows,
            limit=limit,
        )

        if limit and len(rows) >= limit:
            rows.append(["...", "..."])

        return (headers, rows)

    def __getitem__(self, item: Hashable) -> Any:
        return self.get(item)

    def __getattr__(self, attr: str) -> Any:
        return self.get(attr)

    def __setitem__(self, item: Hashable, value: Any) -> None:
        self.set(item, value)

    def __setattr__(self, attr: str, value: Any) -> None:
        self.set(attr, value)

    def __repr__(self) -> str:
        return f"Config{dict.__repr__(self)}"

    def _default_getitem(
        self, item: Hashable, default: Any = BaseConfig()
    ) -> Any:
        """Implements defaultdict feature"""

        if type(default) is BaseConfig:
            default = Config()

        if item not in self:
            if default is None:
                raise KeyError(f"There is no '{item}' key in Config")
            else:
                dict.__setitem__(self, item, default)
        return dict.__getitem__(self, item)
