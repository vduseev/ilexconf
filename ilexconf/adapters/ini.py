from configparser import ConfigParser
from typing import Hashable, Mapping, Any
from io import StringIO

from ilexconf.config import Config
from mapz import Mapz

from .common.address import AddressArg
from .common.decorators import reader, writer


def _load(string: str) -> Mapping[str, Any]:
    parser = ConfigParser()
    parser.read_string(string)

    d = {}
    for s in parser.sections() + ["DEFAULT"]:
        d[s] = {}
        for k in parser[s]:
            d[s][k] = parser[s][k]
    return d


def _str_resolver(string: str) -> bool:
    return "[" not in string or not "]" in string


def _pre_process(data: Mapping[str, Any]) -> Mapping[str, Any]:
    return data


def _dump(data: Mapping[str, Any]) -> str:
    # No matter what mapping was passed as input we convert it to Config
    config = Config(data)

    # Initialize INI config
    ini = ConfigParser()
    for s in config:
        if isinstance(config[s], Mapz):
            ini[s] = config[s].flatten()
        else:
            ini["DEFAULT"][s] = str(config[s])

    # Serialize INI config to string
    output = StringIO()
    ini.write(output)
    return output.getvalue()


@reader(load=_load, str_resolver=_str_resolver, pre_processing=_pre_process)
def from_ini(source: AddressArg, ignore_errors: bool = False):
    """Read INI from string, file or path.

    INI adapter relies on Python's
    `ConfigParser <https://docs.python.org/3/library/configparser.html>`_ when
    working with ``.ini`` configuration files.

    Args:
        source (AddressArg): Source of INI. Accepts file, path or string:

    Returns:
        Config: Returns constructed Config object with the values from INI source.

    Raises:
        TypeError: If ``source`` argument is of wrong type.

    Examples:
        Read from file object:

        >>> from ilexconf import from_ini
        >>> with open("path/to/file", "r") as f:
        >>>     config = from_ini(f)

        Read from Path object:

        >>> path = pathlib.Path("path/to/file")
        >>> config = from_ini(path)

        Read from INI containing string:

        >>> config = from_ini("name = Boris")

        Read from plain string path:

        >>> config = from_ini("path/to/file")

    """
    pass  # pragma: no cover


@writer(dump=_dump)
def to_ini(mapping: Mapping[Hashable, Any], destination: AddressArg):
    """Write data to INI file or convert to INI string

    INI adapter relies on Python's
    `ConfigParser <https://docs.python.org/3/library/configparser.html>`_ when
    working with ``.ini`` configuration files.

    Any top level key of the ``data`` argument is considered to be a section.
    Any subsequent values or nested mappings of each of the top level keys are
    flattened before being written.

    Args:
        data (Mapping): Mapping object to dump to INI.
        destination (optional): Accepts either File (stream), Path or str. Defaults to ``None``.

    Returns:
        str: Returns ``data`` Mapping converted to INI string.

    Raises:
        UnsupportedDataDestinationType: When ``destination`` argument is of wrong type.

    Examples:
        Write to file object:

        >>> from ilexconf import to_ini
        >>> with open("path/to/file", "w") as f:
        >>>     to_ini(config, f)

        Write to stream:

        >>> to_ini(config, sys.stdout)

        Write to Path object:

        >>> to_ini(config, pathlib.Path("path/to/file"))

        Write to string path:

        >>> to_ini(config, "path/to/file")

        Convert to string:

        >>> string = to_ini(config)

    """
    pass  # pragma: no cover
