from mapz import Mapz

from typing import (
    Any,
    Hashable,
    Mapping,
)

class Config(Mapz):
    def __init__(self, *mappings: Mapping[Hashable, Any], **kwargs: Any):
        super().__init__(*mappings)

        for k, v in kwargs.items():
            self.set(
                k,
                v,
                key_prefix="",
                key_sep="__",
            )

    def __repr__(self) -> str:
        return f"Config{dict.__repr__(self)}"
