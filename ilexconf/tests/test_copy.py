from ilexconf import Config, from_json
 
import pytest


def test_copy(settings_json_dict):
    config = Config(settings_json_dict)

    copy = config.copy()

    # Change value in initial object and check it
    config.database.connection.host = "1.2.3.4"
    assert config.database.connection.host == "1.2.3.4"

    # Make sure value in copied object has not changed
    assert copy.database.connection.host == "localhost"
