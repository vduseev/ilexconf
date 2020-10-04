from ilexconf import Config, from_json, to_json

# from ilexconf.tests.debug import debug

import os
import pytest


FIXTURE_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), "files")


@pytest.fixture(scope="module")
def settings_json_dict():
    return {"database": {"connection": {"host": "localhost", "port": 5432}}}


@pytest.fixture(scope="module")
def settings_json_file_path():
    return os.path.join(FIXTURE_DIR, "settings.json")


@pytest.fixture(scope="module")
def resulting_dict():
    return {
        "database": {
            "connection": {
                "host": "test.local",
                "port": 8080,
                "user": "root",
                "password": "different secret",
            }
        }
    }


def test_quick_start(
    settings_json_dict, settings_json_file_path, resulting_dict, tmp_path
):
    # Single instance of config shared between all tests in this module
    config = Config()

    # CREATE
    #########

    # Create configuration using JSON file, dictionary and key-value pair
    config = Config(
        from_json(settings_json_file_path),
        {"database": {"connection": {"host": "test.local"}}},
        database__connection__port=4000,
    )

    # Check it was created and values are merged properly
    assert config.as_dict() == {
        "database": {"connection": {"host": "test.local", "port": 4000}}
    }

    # READ
    #######

    # from ilexconf import (
    #     from_json,
    #     # from_yaml,
    #     # from_toml,
    #     from_ini,
    #     # from_python,
    #     # from_dotenv,
    #     from_env,
    # )

    cfg1 = from_json(settings_json_file_path)
    assert cfg1.as_dict() == settings_json_dict

    # cfg2 = Config(
    #     from_yaml("settings.yaml"),
    #     from_toml("settings.toml")
    # )

    # cfg3 = Config(
    #     from_ini("settings.ini"),
    #     from_python("settings.py"),
    #     from_dotenv(".env"),
    #     from_env()
    # )

    # ACCESS
    #########

    # Classic way
    print(config.as_dict())
    assert config["database"]["connection"]["host"] == "test.local"

    # Dotted key
    assert config["database.connection.host"] == "test.local"

    # Attributes
    assert config.database.connection.host == "test.local"

    # Any combination of the above
    assert config["database"].connection.host == "test.local"
    assert config.database["connection.host"] == "test.local"
    assert config.database["connection"].host == "test.local"
    assert config.database.connection["host"] == "test.local"

    # CHANGE & CREATE
    ##################

    # Classic way
    config["database"]["connection"]["port"] = 8080
    assert config["database"]["connection"]["port"] == 8080

    # Dotted key (that does not exist yet)
    config["database.connection.user"] = "root"
    assert config["database.connection.user"] == "root"

    # Attributes (also does not exist yet)
    config.database.connection.password = "secret stuff"
    assert config.database.connection.password == "secret stuff"

    # MERGE
    ########

    config.database.connection.merge({"password": "different secret"})
    assert config.database.connection.password == "different secret"

    # AS_DICT
    ##########

    assert config.as_dict() == resulting_dict

    # WRITE
    ########

    # Temporary path
    p = tmp_path / "settings.json"
    # Save config
    to_json(config, str(p))
    # Verify written file is correct
    assert from_json(str(p)).as_dict() == resulting_dict

    # SUBCLASSING
    ##############

    class MyConfig(Config):
        def __init__(self, do_stuff=False):
            # Initialize your custom config with JSON by default
            super().__init__(self, from_json(settings_json_file_path))

            # Add some custom value depending on some logic
            if do_stuff:
                self.my.custom.key = "Yes, do stuff"

            self.merge({"Horizon": "Up"})

    # Now you can use your custom Configuration everywhere
    config = MyConfig(do_stuff=True)
    assert config.my.custom.key == "Yes, do stuff"
    assert config.Horizon == "Up"
