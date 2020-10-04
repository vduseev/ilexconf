import os
import json

from ilexconf.config import Config
from ilexconf.helpers import keyval_to_dict

from typing import Any, Mapping, Dict, Union, TextIO


def from_env(prefix="", separator="__", lowercase=False):
    """
    Read config from environment variables.
    """
    config = Config()

    for k, v in os.environ.items():
        if prefix and not k.startswith(prefix):
            # If prefix is specified, then ignore the values without it
            continue

        # Strip key off of prefix
        prefixless_key = k[len(prefix) :]
        # Lowercase key if needed
        key = k.lower() if lowercase else k
        # Convert current key-value pair to Mapping
        d = keyval_to_dict(key, v, prefix=prefix, separator=separator)
        # Merge this Mapping into config
        config.merge(d)

    return config


def to_env(data: Mapping[Any, Any]):
    """
    Set environment variales for child processes invoked using
    methods like os.system(), popen() or fork() and execv().
    """
    config = Config(data)


def from_json(data: Union[str, TextIO], read_from_file: bool = True):
    """
    Read data from JSON file or JSON string.
    """
    if read_from_file:
        if isinstance(data, str):
            json_dict = json.load(open(data, "rt"))
        else:
            json_dict = json.load(data)
    else:
        json_dict = json.loads(str(data))

    config = Config(json_dict)
    return config


def to_json(data: Mapping[Any, Any], path: str):
    """
    Write data to JSON file.
    """
    if isinstance(data, Config):
        data = data.as_dict()
    with open(path, "w") as f:
        json.dump(data, f, indent=2)


def from_ini(
    data: Union[str, TextIO], read_from_file: bool = False, lowercase_keys: bool = False
):
    """
    Read data from INI file or INI string.
    """
    import configparser

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
