from json import load, loads, dumps

from .decorators import reader, writer


@reader(
    file_load=lambda data: load(data),
    path_load=lambda data: load(data.open("rt")),
    string_load=lambda data: loads(data) if "{" in data and "}" in data else load(open(data, "rt"))
)
def from_json():
    """Read JSON from string, file or path.
    
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


@writer(
    dump=lambda data, **kwargs: dumps(data, **kwargs),
    indent=2
)
def to_json():
    """Write data to JSON file or convert to JSON string
    
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
    
