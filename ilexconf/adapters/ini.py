import configparser

from typing import Union, TextIO


def from_ini(
    data: Union[str, TextIO], read_from_file: bool = False, lowercase_keys: bool = False
):
    """
    Read data from INI file or INI string.
    """
    if read_from_file:
        if isinstance(data, str):
            data = open(data, "rt").read()
        else:
            data = data.read()
    data = str(data)
    cfg = configparser.RawConfigParser()
    cfg.read_string(data)
    result = {
        section + "." + k: v
        for section, values in cfg.items()
        for k, v in values.items()
    }
