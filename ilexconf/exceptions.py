from typing import Any


class UnsupportedDataSourceType(Exception):
    def __init__(self, arg: Any) -> None:
        self.arg = arg
        self.typ = type(arg)
        self.msg = f"Type {self.typ} of {self.arg} is not supported as source"
        super().__init__(self, self.msg)

class UnsupportedDataDestinationType(Exception):
    def __init__(self, arg: Any) -> None:
        self.arg = arg
        self.typ = type(arg)
        self.msg = f"Type {self.typ} of {self.arg} is not supported as destination"
        super().__init__(self, self.msg)
