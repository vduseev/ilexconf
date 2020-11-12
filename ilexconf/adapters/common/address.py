from enum import Enum, auto

from typing import Union, Callable
from io import TextIOBase
from pathlib import Path


AddressArg = Union[str, Path, TextIOBase]
StrResolver = Callable[[str], bool]


class AddressType(Enum):
    """Type of source or destination.

    Provides built-in methods to load/write from/to any of the supported
    source and destination types.

    Attributes:
        STRING (int): Load from string or return as string.
        STRING_PATH (int): Load from path represented as a string or write to
            such path.
        PATH (int): Load from path represented as pathlib.Path object or
            write to such path.
        STREAM (int): Load from stream represented as file-like object such as
            sys.stdout, open(), StringIO(); or write to such object.
    """

    STRING = auto()
    STRING_PATH = auto()
    PATH = auto()
    STREAM = auto()


class Address:
    """"""

    @staticmethod
    def read(source: AddressArg, str_resolver: StrResolver = None) -> str:
        # Determine type of the source argument
        source_type = Address._resolve(source, str_resolver)

        # Read from this type of soure using proper mapped method
        data = Address._read_method(source_type)(source)

        return data

    @staticmethod
    def write(
        data: str,
        destination: AddressArg = None,
        str_resolver: StrResolver = None,
    ) -> None:
        # Determine type of the destination argument
        destination_type = Address._resolve(destination, str_resolver)

        # Write to this destination using a proper mapped method
        result = Address._write_method(destination_type)(data, destination)

        return result

    @staticmethod
    def _resolve(
        address: AddressArg, str_resolver: StrResolver = None
    ) -> int:
        """Determine which type the ``data`` argument belongs to.

        Args:
            address (AddressArg): Source or destination to read or write data.
            str_resolver (StrResolver): Checker function that
                determines whether the ``data`` argument represents a string
                containing the configuration or a string containing a path to
                configuration file. Only applied when ``data`` is str.

        Returns:
            AddressType: Type of address contained in ``data`` argument.

        Raises:
            TypeError: When address of the ``data`` argument could not be determined.

        """

        str_resolver = str_resolver or Address._dummy_str_resolver

        if isinstance(address, str):
            if str_resolver(address):
                return AddressType.STRING_PATH
            else:
                return AddressType.STRING
        elif isinstance(address, Path):
            return AddressType.PATH
        elif isinstance(address, TextIOBase):
            return AddressType.STREAM
        elif address is None:
            return AddressType.STRING
        else:
            raise TypeError(
                f"Type {type(address)} of {address} is not supported as address of source or destination"
            )

    @staticmethod
    def _from_string(string: str) -> str:
        return string

    @staticmethod
    def _from_string_path(string: str) -> str:
        result = None
        with open(string, "rt") as f:
            result = f.read()
        return result

    @staticmethod
    def _from_path(path: Path) -> str:
        result = path.read_text()
        return result

    @staticmethod
    def _from_stream(stream: TextIOBase) -> str:
        result = stream.read()
        return result

    @staticmethod
    def _to_string(data: str, string: str) -> str:
        return data

    @staticmethod
    def _to_string_path(data: str, string: str) -> str:
        with open(string, "w") as f:
            f.write(data)
        return data

    @staticmethod
    def _to_path(data: str, path: Path) -> str:
        with path.open("w") as f:
            f.write(data)
        return data

    @staticmethod
    def _to_stream(data: str, stream: TextIOBase) -> str:
        stream.write(data)
        return data

    @staticmethod
    def _dummy_str_resolver(string: str) -> bool:
        return False

    @staticmethod
    def _read_method(typ: AddressType):
        mapping = {
            AddressType.STRING: Address._from_string,
            AddressType.STRING_PATH: Address._from_string_path,
            AddressType.PATH: Address._from_path,
            AddressType.STREAM: Address._from_stream,
        }
        return mapping[typ]

    @staticmethod
    def _write_method(typ: AddressType):
        mapping = {
            AddressType.STRING: Address._to_string,
            AddressType.STRING_PATH: Address._to_string_path,
            AddressType.PATH: Address._to_path,
            AddressType.STREAM: Address._to_stream,
        }
        return mapping[typ]
