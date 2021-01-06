from typing import Any, Hashable, Mapping
from .common.address import AddressArg
import sys
import os
from io import StringIO
from mapz import Mapz


try:
    # Special case for pytest coverage
    if "_pytest_yaml_test_pyyaml" in os.environ:
        raise ImportError()

    from ruamel.yaml import YAML

    yaml = YAML()
    yaml_load = yaml.load
except ImportError:
    try:
        # Special case for pytest coverage
        if "_pytest_yaml_test_noyaml" in os.environ:
            raise ImportError()

        import yaml

        yaml_load = yaml.safe_load
    except ImportError:
        yaml = None

from .common.decorators import reader, writer


def from_yaml(*args, **kwargs):
    raise NotImplementedError(
        "ruamel.yaml or PyYaml must be installed in order to use YAML adapter"
    )


def to_yaml(*args, **kwargs):
    raise NotImplementedError(
        "ruamel.yaml or PyYaml must be installed in order to use YAML adapter"
    )


if yaml:

    def _load(data: str):
        # If data is a string in a form of
        # "name: boris" or "name:" then it will
        # be parsed by yaml module to a str instance.
        d = yaml_load(data)

        # Do not accept plain string yaml files
        # as configs. Treat such strings as paths.
        if isinstance(d, str):
            with open(data, "rt") as f:
                d = yaml_load(f)

        return d

    def _dump(data, **kwargs) -> str:
        stream = StringIO()

        yaml.dump(data, stream, **kwargs)
        dumped = stream.getvalue()

        return dumped

    @reader(load=_load)
    def from_yaml(source: AddressArg, ignore_errors: bool = False):
        """Read data from YAML string, file object or path"""
        pass  # pragma: no cover

    @writer(dump=_dump)
    def to_yaml(mapping: Mapping[Hashable, Any], destination: AddressArg):
        """Write data to YAML file or convert to YAML string"""
        pass  # pragma: no cover
