from json import load, loads, dumps

from .decorators import reader, writer


@reader(
    file_load=lambda data: load(data),
    path_load=lambda data: load(data.open("rt")),
    string_load=lambda data: loads(data) if "{" in data and "}" in data else load(open(data, "rt"))
)
def from_json():
    """Read JSON from string, file or path"""
    pass  # pragma: no cover


@writer(
    string_dump=lambda data: dumps(data)
)
def to_json(indent: int = 2):
    """Write data to JSON file or convert to JSON string"""
    pass  # pragma: no cover
    
