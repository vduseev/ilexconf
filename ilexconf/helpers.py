from enum import Enum, auto
from pathlib import Path
from typing import Dict, Union, TextIO
from io import IOBase

from ilexconf.exceptions import UnknownDataSourceArgumentType, UnknownDataDestinationArgumentType


def keyval_to_dict(key, value, prefix="", separator="__", lowercase=False) -> Dict:
    """Transform key-value into Mapping"""

    if prefix and not key.startswith(prefix):
        # if prefix is specified, then return nothing for keys without it
        return {}

    # strip key off of prefix
    prefixless_key = key[len(prefix) :]
    # lowercase key if needed
    key = prefixless_key.lower() if lowercase else prefixless_key
    prefix = prefix.lower() if lowercase else prefix

    parts = key.strip(separator).split(separator, maxsplit=1) if separator else key
    if isinstance(parts, list) and len(parts) > 1:
        k, subkey = parts  # unpack split parts for readability
        return {k: keyval_to_dict(subkey, value, prefix="", separator=separator)}
    elif isinstance(parts, list) and len(parts) == 1:
        # Special case for Issue#21
        return {parts[0]: value}
    else:
        return {parts: value}

class DataSource(Enum):
    STRING = auto()
    FILE = auto()
    PATH = auto()

    @staticmethod
    def determine(data: Union[str, TextIO, Path]):
        if isinstance(data, Path):
            return DataSource.PATH
        elif isinstance(data, TextIO):
            return DataSource.FILE
        elif isinstance(data, str):
            return DataSource.STRING
        else:
            raise UnknownDataSourceArgumentType()


class DataDestination(Enum):
    PATH = auto()
    STRING_PATH = auto()
    STREAM = auto()

    @staticmethod
    def determine(data: Union[Path, str, IOBase]):
        if isinstance(data, Path):
            return DataDestination.PATH
        elif isinstance(data, IOBase):
            return DataDestination.STREAM
        elif isinstance(data, str):
            return DataDestination.STRING_PATH
        else:
            raise UnknownDataDestinationArgumentType()
