from functools import wraps
from pathlib import Path

from ilexconf.config import Config
from ilexconf.helpers import DataSource, DataDestination
from ilexconf.exceptions import UnsupportedDataSourceType, UnsupportedDataDestinationType

from typing import Union, TextIO, Mapping, Any
from io import IOBase


def reader(file_load=None, path_load=None, string_load=None, post_processing=lambda d: d):

    def decorator_reader(func):
    
        @wraps(func)
        def wrapper_reader(data: Union[str, TextIO, Path], **kwargs):
            source = DataSource.determine(data)

            d = None
            if source is DataSource.FILE:
                d = file_load(data)

            elif source is DataSource.PATH:
                d = path_load(data)

            elif source is DataSource.STRING:
                d = string_load(data)

            else:
                raise UnsupportedDataSourceType()

            # Perform any postprocessing necessary
            d = post_processing(d)

            config = Config.parse(d)
            return config

        return wrapper_reader

    return decorator_reader


def writer(string_dump=None):

    def decorator_writer(func):

        @wraps(func)
        def wrapper_writer(data: Mapping[Any, Any], destination: Union[str, Path, IOBase] = None, **kwargs):
            if isinstance(data, Config):
                data = data.as_dict()

            # Convert mapping to string
            s = string_dump(data)

            # Without destination specified just return the string
            if destination is None:
                return s

            dest = DataDestination.determine(destination) 
            if dest is DataDestination.PATH:
                with destination.open("w") as f:
                    f.write(s)
                    
            elif dest is DataDestination.STRING_PATH:
                with open(destination, "w") as f:
                    f.write(s)

            elif dest is DataDestination.STREAM:
                destination.write(s)

            else:
                raise UnsupportedDataDestinationType()

        return wrapper_writer

    return decorator_writer
