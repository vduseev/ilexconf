import os
import pytest

from ilexconf import Config, from_json, to_json

# from ilexconf.tests.debug import debug


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
    # os.putenv("AWS_DEFAULT_REGION", "us-east-1")
    os.environ["AWS_DEFAULT_REGION"] = "us-east-1"

    # [create]
    from ilexconf import Config, from_json, from_env, to_json

    # Empty config
    config = Config()
    assert config.as_dict() == {}

    # Create config from json and merge it into our initial config
    # Let settings_json_file_path = "settings.json" where inside the file we have
    # { "database": { "connection": { "host": "localhost", "port": 5432 } } }
    config.merge(from_json(settings_json_file_path))
    assert config.as_dict() == {
        "database": {"connection": {"host": "localhost", "port": 5432}}
    }

    # Merge dict into config
    config.merge({"database": {"connection": {"host": "test.local"}}})
    assert config.as_dict() == {
        "database": {"connection": {"host": "test.local", "port": 5432}}
    }

    # Merge environment variables into config
    config.merge(from_env(prefix="AWS_", separator="__", lowercase=True))
    assert config.as_dict() == {
        "database": {"connection": {"host": "test.local", "port": 5432}},
        "default_region": "us-east-1",
    }

    # Merge keyword arguments
    config.merge(my__keyword__argument=True)
    assert config.as_dict() == {
        "database": {"connection": {"host": "test.local", "port": 5432}},
        "default_region": "us-east-1",
        "my": {"keyword": {"argument": True}},
    }

    # Clear values, just like with dict
    config.clear()
    assert config.as_dict() == {}

    # Or, better yet, do this all in one step, since Config() constructor
    # accepts any number of mapping objects and keyword arguments as
    # initialization parameters. However, order of parameters matters.
    # Last mappings are merged on top of others. And keywords override even that.
    config = Config(
        from_json(settings_json_file_path),
        {"database": {"connection": {"host": "test.local"}}},
        database__connection__port=4000,
    )
    assert config.as_dict() == {
        "database": {"connection": {"host": "test.local", "port": 4000}}
    }
    # [create]

    # from ilexconf import (
    #     from_json,
    #     # from_yaml,
    #     # from_toml,
    #     from_ini,
    #     # from_python,
    #     # from_dotenv,
    #     from_env,
    # )
    # [read]
    cfg1 = from_json(settings_json_file_path)
    assert cfg1.as_dict() == {
        "database": {"connection": {"host": "localhost", "port": 5432}}
    }
    # [read]

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

    # [access]
    # Classic way
    assert config["database"]["connection"]["host"] == "test.local"

    # Dotted key notation
    assert config["database.connection.host"] == "test.local"

    # Via attributes
    assert config.database.connection.host == "test.local"

    # Any combination of the above
    assert config["database"].connection.host == "test.local"
    assert config.database["connection.host"] == "test.local"
    assert config.database["connection"].host == "test.local"
    assert config.database.connection["host"] == "test.local"
    # [access]

    # [upsert]
    # Change value that already exists in the dictionary
    # just like you would do with simple dict
    config["database"]["connection"]["port"] = 8080
    assert config["database"]["connection"]["port"] == 8080

    # Create new value using 'dotted notation'. Notice that
    # 'user' field did not exist before.
    config["database.connection.user"] = "root"
    assert config["database.connection.user"] == "root"

    # Create new value using. 'password' field did not exist
    # before we assigned a value to it and was created automatically.
    config.database.connection.password = "secret stuff"
    assert config.database.connection.password == "secret stuff"
    # [upsert]

    # [merge]
    # Config correctly merges nested values. Notice how it overrides
    # the value of the 'password' key in the nested 'connection' config
    # from 'secret stuff' to 'different secret'
    config.database.connection.merge({"password": "different secret"})
    assert config.database.connection.password == "different secret"
    # [merge]

    # [smart-merge]
    merged = Config({"a1": {"c1": 1, "c2": 2, "c3": 3}}, {"a1": {"c3": "other"}})

    # Instead of overriding the value of the "a1" key completely, `merge` method
    # will recursively look inside and merge nested values.
    assert merged.as_dict() == {"a1": {"c1": 1, "c2": 2, "c3": "other"}}
    # [smart-merge]

    # [as-dict]
    assert config.as_dict() == {
        "database": {
            "connection": {
                "host": "test.local",
                "port": 8080,
                "user": "root",
                "password": "different secret",
            }
        }
    }
    # [as-dict]

    # [write]
    # Temporary path
    p = tmp_path / "settings.json"
    # Save config
    to_json(config, str(p))
    # Verify written file is correct
    assert from_json(str(p)).as_dict() == {
        "database": {
            "connection": {
                "host": "test.local",
                "port": 8080,
                "user": "root",
                "password": "different secret",
            }
        }
    }
    # [write]

    # [subclass]
    class MyConfig(Config):
        def __init__(self, do_stuff=False):
            # Initialize your custom config using json settings file
            super().__init__(self, from_json(settings_json_file_path))

            # Add some custom value depending on some logic
            if do_stuff:
                # Here, we create new nested key that did not exist
                # before and assign a value to it.
                self.my.custom.key = "Yes, do stuff"

            # Merge one more mapping on top
            self.merge({"Horizon": "Up"})

    # [subclass]

    # [test-subclass]
    # Now you can use your custom defined Config. Given the `setting.json` file that
    # contains { "database": { "connection": { "host": "localhost", "port": 5432 } } }
    # MyConfig will have the following values:

    config = MyConfig(do_stuff=True)
    print(config.as_dict())
    assert config.as_dict() == {
        "database": {
            "connection": {
                "host": "localhost",
                "port": 5432,
            },
        },
        "Horizon": "Up",
        "my": {"custom": {"key": "Yes, do stuff"}},
    }
    # [test-subclass]
