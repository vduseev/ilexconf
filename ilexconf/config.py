from mapz import Mapz

from typing import (
    Any,
    Dict,
    Hashable,
    Mapping,
)


class Config(Mapz):
    def __init__(self, *mappings: Mapping[Hashable, Any], **kwargs: Dict):
        super().__init__(*mappings)

        for k, v in kwargs.items():
            self.set(
                k,
                v,
                key_prefix="",
                key_sep="_",
            )

    def __repr__(self) -> str:
        return f"Config{dict.__repr__(self)}"
