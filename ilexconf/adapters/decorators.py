from functools import wraps
from pathlib import Path
from enum import Enum, auto
from io import IOBase

from ilexconf.config import Config
from ilexconf.exceptions import UnsupportedDataSourceType, UnsupportedDataDestinationType

from typing import Union, TextIO, Mapping, Any


class DataSource(Enum):
    STRING = auto()
    FILE = auto()
    PATH = auto()

    @staticmethod
    def determine(data: Union[str, IOBase, Path]):
        if isinstance(data, Path):
            return DataSource.PATH
        elif isinstance(data, IOBase):
            return DataSource.FILE
        elif isinstance(data, str):
            return DataSource.STRING
        else:
            raise UnsupportedDataSourceType(data)


class DataDestination(Enum):
    PATH = auto()
    STRING_PATH = auto()
    STREAM = auto()
    STRING = auto()

    @staticmethod
    def determine(data: Union[Path, str, IOBase]):
        if isinstance(data, Path):
            return DataDestination.PATH
        elif isinstance(data, IOBase):
            return DataDestination.STREAM
        elif isinstance(data, str):
            return DataDestination.STRING_PATH
        elif data is None:
            return DataDestination.STRING
        else:
            raise UnsupportedDataDestinationType(data)


def reader(file_load=None, path_load=None, string_load=None, pre_processing=lambda d: d):

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

            # Perform any pre processing necessary
            d = pre_processing(d)

            config = Config.parse(d)
            return config

        return wrapper_reader

    return decorator_reader


def writer(dump=None, **kwargs):

    def decorator_writer(func):

        @wraps(func)
        def wrapper_writer(data: Mapping[Any, Any], destination: Union[str, Path, IOBase] = None, **given_kwargs):
            if isinstance(data, Config):
                data = data.as_dict()

            # Merge kwargs passed as argument to adapter on top of
            # default kwargs
            kwargs.update(given_kwargs)

            # Convert mapping to string
            s = dump(data, **kwargs)

            dest = DataDestination.determine(destination) 
            if dest is DataDestination.PATH:
                with destination.open("w") as f:
                    f.write(s)
                    
            elif dest is DataDestination.STRING_PATH:
                with open(destination, "w") as f:
                    f.write(s)

            elif dest is DataDestination.STREAM:
                destination.write(s)

            elif dest is DataDestination.STRING:
                return s

            return s

        return wrapper_writer

    return decorator_writer
