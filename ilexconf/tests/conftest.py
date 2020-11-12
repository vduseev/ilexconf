import os
import pytest


@pytest.fixture(scope="session", autouse=True)
def fixture_dir():
    return os.path.join(
        os.path.dirname(os.path.realpath(__file__)), "resources"
    )


@pytest.fixture(scope="session", autouse=True)
def settings_json_dict():
    return {"database": {"connection": {"host": "localhost", "port": 5432}}}


@pytest.fixture(scope="session", autouse=True)
def settings_json_string():
    return '{ "database": { "connection": { "host": "localhost", "port": 5432 } } }'


@pytest.fixture(scope="session", autouse=True)
def settings_json_file_path(fixture_dir):
    return os.path.join(fixture_dir, "settings.json")
