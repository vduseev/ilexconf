import sys
import pytest
from pathlib import Path

from ilexconf.adapters.decorators import DataSource, DataDestination
from ilexconf.exceptions import UnsupportedDataSourceType, UnsupportedDataDestinationType


def test_data_source(settings_json_file_path):
    # File
    with open(settings_json_file_path, "rt") as f:
        assert DataSource.determine(f) is DataSource.FILE

    # Path
    assert DataSource.determine(Path("settings.json")) is DataSource.PATH

    # String
    assert DataSource.determine("settings.json") is DataSource.STRING

    # Unknown argument
    with pytest.raises(UnsupportedDataSourceType):
        DataSource.determine(132)


def test_data_destination(settings_json_file_path):
    # Path
    assert DataDestination.determine(Path("settings.json")) is DataDestination.PATH

    # String path
    assert DataDestination.determine("settings.json") is DataDestination.STRING_PATH

    # Stream
    assert DataDestination.determine(sys.stdout) is DataDestination.STREAM

    # Unknown
    with pytest.raises(UnsupportedDataDestinationType):
        DataDestination.determine(1000)
