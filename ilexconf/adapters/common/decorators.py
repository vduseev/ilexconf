from functools import wraps

from ilexconf.config import Config
from .address import Address, AddressArg, StrResolver

from typing import Callable, Mapping, Any

LoadCallable = Callable[[AddressArg], str]
DumpCallable = Callable[[Mapping[Any, Any]], str]
PreProcessingCallable = Callable[[Mapping[Any, Any]], Mapping[Any, Any]]


def _dummy_load(string: str) -> str:
    return string


def _dummy_pre_processing(data: Mapping[Any, Any]) -> Mapping[Any, Any]:
    return data


def _dummy_dump(data: Mapping[Any, Any], **kwargs) -> str:
    return str(data)


def reader(
    load: LoadCallable = _dummy_load,
    str_resolver: StrResolver = None,
    pre_processing: PreProcessingCallable = _dummy_pre_processing
):
    """Decorator for read adapter functions such as ``from_``.

    Args:
        load: Function that loads certain format from string and returns a Mapping.
        str_resolver: Function that determines whether str data passed to decorated function is a path to file or not.
        pre_processing: Function that somehow transforms Mapping obtained from ``load`` before passing it to ``Config`` constructor.
    """

    def decorator_reader(func):
        @wraps(func)
        def wrapper_reader(data: AddressArg, **kwargs):
            # Read data using proper loader
            serialized = Address.read(data, str_resolver)

            # Parse string data to dictionary using provided ``load``
            # callable argument.
            deserialized = load(serialized, **kwargs)

            # Perform any pre processing necessary with the parsed
            # dictionary
            deserialized = pre_processing(deserialized)

            config = Config._parse_value(deserialized)
            return config

        return wrapper_reader

    return decorator_reader


def writer(dump: DumpCallable = _dummy_dump, **default_kwargs):
    """Decorator for write adapter functions such as ``to_``.

    Args:
        dump: Function that serializes mapping to a string.
        **default_kwargs: Default keyword arguments that will be passed to the ``dump`` function.
    """

    def decorator_writer(func):
        @wraps(func)
        def wrapper_writer(
            data: Mapping[Any, Any], destination: AddressArg = None, **kwargs
        ):
            if isinstance(data, Config):
                data = data.as_dict()

            # Merge kwargs passed as argument to adapter on top of
            # default kwargs
            merged_kwargs = default_kwargs.copy()
            merged_kwargs.update(kwargs)

            # Convert mapping to string using provided ``dump`` callable
            # argument.
            serialized = dump(data, **merged_kwargs)

            # Save dumped string to destination.
            Address.write(serialized, destination, str_resolver=None)

            # Always return converted (dumped) string.
            return serialized

        return wrapper_writer

    return decorator_writer
