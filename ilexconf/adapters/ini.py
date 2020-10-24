from configparser import ConfigParser
from pathlib import Path
from typing import TextIO, Union

from .decorators import reader, writer


def _file_loader(data: Union[TextIO, Path]):
    parser = ConfigParser()
    return parser.read([data])


def _string_loader(data: str):
    parser = ConfigParser()
    return parser.read_string(data)


@reader(
    file_load=_file_loader,
    path_load=_file_loader,
    string_load=_string_loader,
    pre_processing=lambda data: { section + "." + k: v for section, values in data.items() for k, v in values.items() }
)
def from_ini():
    """Read data from INI string, file object or path"""
    pass  # pragma: no cover


@writer(
    dump=None
)
def to_ini():
    """Write data to INI file or convert to YAML string"""
    pass  # pragma: no cover
