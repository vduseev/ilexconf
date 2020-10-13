import json

from ilexconf.config import Config

from typing import Union, TextIO, Mapping, Any


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
