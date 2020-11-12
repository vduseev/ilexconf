import os

from ilexconf.config import Config

from typing import Mapping, Any, Union


def from_env(prefix="", separator="__"):
    """Read config from environment variables."""

    prefix = "" if prefix is None else prefix
    config = Config()

    for k, v in os.environ.items():
        # Convert current key-value pair to Mapping
        config.set(k, v, key_prefix=prefix, key_sep=separator)

    return config


def to_env(data: Config, prefix="", separator="__"):
    """Export mapping to environment variables.

    This will set the environment variable both for current python
    context as well as for child processes invoed via os.system(),
    popen(), fork(), and execv().

    :param data: Mapping object to export.
    :type data: Mapping[Any, Any]
    """

    config = Config(data)

    # Convert entire hierarchy to flat keys with values.
    # { "database": { "connection": { "host": "1.2.3.4" }}} will turn into
    # { "my_database__connection__host": "1.2.3.4" } with prefix == "my_"
    # and separator == "__".
    flat = config.flatten()

    for k, v in flat.items():
        key = prefix + k.replace(".", separator)

        # Set environment variable for current context
        os.environ[key] = v
        os.putenv(key, v)
