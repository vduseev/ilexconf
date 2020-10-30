import os

from ilexconf.config import Config

from typing import Mapping, Any, Union


def from_env(prefix="", separator="__", lowercase=False, uppercase=False):
    """Read config from environment variables.
    """

    prefix = "" if prefix is None else prefix
    config = Config()

    for k, v in os.environ.items():
        # Convert current key-value pair to Mapping
        d = Config.from_keyvalue(
            k, v, prefix=prefix, sep=separator, lowercase=lowercase, uppercase=uppercase
        )
        # Merge this Mapping into config
        config.merge(d)

    return config


def to_env(
    data: Mapping[Any, Any], prefix="", separator="__", uppercase=False, lowercase=False
):
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
    prefix = prefix.upper() if uppercase else prefix.lower() if lowercase else prefix

    for k, v in flat.items():
        adjusted_k = k.upper() if uppercase else k.lower() if lowercase else k
        key = prefix + adjusted_k.replace(".", separator)

        # Set environment variable for current context
        os.environ[key] = v
        os.putenv(key, v)
