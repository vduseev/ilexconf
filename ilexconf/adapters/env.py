import os

from ilexconf.config import Config
from ilexconf.helpers import keyval_to_dict

from typing import Mapping, Any, Union


def from_env(prefix="", separator="__", lowercase=False):
    """Read config from environment variables.

    :param prefix: Prefix to environment variables, defaults to ""
    :type prefix: str, optional
    :param separator: Delimiter by which variable is separated and turned into a nested object, defaults to "__"
    :type separator: str, optional
    :param lowercase: Convert names of variable to lowercase, defaults to False
    :type lowercase: bool, optional
    :return: Config object
    :rtype: Config
    """
    prefix = "" if prefix is None else prefix
    config = Config()

    for k, v in os.environ.items():
        # Convert current key-value pair to Mapping
        d = keyval_to_dict(
            k, v, prefix=prefix, separator=separator, lowercase=lowercase
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
