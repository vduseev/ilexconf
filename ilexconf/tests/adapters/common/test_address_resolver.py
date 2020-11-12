import sys
import pytest
from pathlib import Path

from ilexconf.adapters.common.address import AddressType, Address


def test_resolver(settings_json_file_path):
    # File
    with open(settings_json_file_path, "rt") as f:
        assert Address._resolve(f) is AddressType.STREAM

    # Stdout
    assert Address._resolve(sys.stdout) is AddressType.STREAM

    # Path
    assert Address._resolve(Path("settings.json")) is AddressType.PATH

    # String
    assert (
        Address._resolve("settings.json", lambda string: False)
        is AddressType.STRING
    )

    # String Path
    assert (
        Address._resolve("settings.json", lambda string: True)
        is AddressType.STRING_PATH
    )

    # None
    assert Address._resolve(None) is AddressType.STRING

    # Unknown argument
    with pytest.raises(TypeError):
        Address._resolve(132)
