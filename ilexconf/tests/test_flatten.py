from ilexconf import Config

import pytest


def test_simple_flatten(settings_json_dict):
    config = Config(settings_json_dict)

    flat = config.flatten()
    assert flat == {
        "database.connection.host": "localhost",
        "database.connection.port": 5432,
    }


def test_list_flatten():
    pass
