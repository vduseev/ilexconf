from .common.address import AddressArg
from json import loads, dumps
from typing import Hashable, Mapping, Any

from .common.decorators import reader, writer


def _load(string) -> Mapping[str, Any]:
    parsed = loads(string)
    return parsed


def _dump(data: Mapping[Any, Any], **kwargs) -> str:
    dumped = dumps(data, **kwargs)
    return dumped


@reader(
    load=_load,
    str_resolver=lambda string: "{" not in string or "}" not in string,
)
def from_json(source: AddressArg, ignore_errors: bool = False):
    """Read JSON from string, file or path.

    JSON adapter relies on Python's
    `json <https://docs.python.org/3/library/json.html>`_ module when
    working with ``.json`` files.

    Args:
        data: Source of JSON. Accepts file, path or string:

    Returns:
        Config: Returns constructed Config object with the values from JSON source.

    Raises:
        UnsupportedDataSourceType: If ``data`` argument is of wrong type.

    Examples:
        Read from file object:

        >>> from ilexconf import from_json
        >>> with open("path/to/file", "r") as f:
        >>>     config = from_json(f)

        Read from Path object:

        >>> path = pathlib.Path("path/to/file")
        >>> config = from_json(path)

        Read from JSON string:

        >>> config = from_json('{ "name": "Boris" }')

        Read from plain string path:

        >>> config = from_json("path/to/file")

    """
    pass  # pragma: no cover


@writer(dump=_dump, indent=2)
def to_json(mapping: Mapping[Hashable, Any], destination: AddressArg):
    """Write data to JSON file or convert to JSON string

    JSON adapter relies on Python's
    `json <https://docs.python.org/3/library/json.html>`_ module when
    working with ``.json`` files.

    Args:
        data (Mapping): Mapping object to dump to JSON.
        destination (optional): Accepts either File (stream), Path or str. Defaults to ``None``.
        indent (:obj:`int`, optional): Indentation for JSON. Defaults to 2.
            Use ``indent=None`` to convert without indentation.
        **kwargs: Any other keyword arguments accepted by
            `json.dumps() <https://docs.python.org/3/library/json.html#json.dumps>`_ method.

    Returns:
        str: Returns ``data`` Mapping converted to JSON string.

    Raises:
        UnsupportedDataDestinationType: When ``destination`` argument is of wrong type.

    Examples:
        Write to file object:

        >>> from ilexconf import to_json
        >>> with open("path/to/file", "w") as f:
        >>>     to_json(config, f)

        Write to stream:

        >>> to_json(config, sys.stdout)

        Write to Path object:

        >>> to_json(config, pathlib.Path("path/to/file"))

        Write to string path:

        >>> to_json(config, "path/to/file")

        Convert to string:

        >>> string = to_json(config)

    """
    pass  # pragma: no cover
