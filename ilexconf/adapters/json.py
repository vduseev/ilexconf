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


def to_json(data: Mapping[Any, Any], path: str = None, indent: int = 2):
    """
    Convert data to JSON and optionally write to file.
    """
    if isinstance(data, Config):
        data = data.as_dict()

    # Convert data to json
    json_data = json.dumps(data, indent=indent)

    if path:
        with open(path, "w") as f:
            f.write(json_data)

    return json_data
