from ilexconf.config import Config
from ilexconf.adapters.common.decorators import (
    _dummy_load,
    _dummy_dump,
    _dummy_pre_processing,
    reader,
    writer,
)


@reader(
    load=lambda string: {"name": string},
    str_resolver=lambda string: False,
    pre_processing=lambda mapping: {
        k: v for k, v in list(mapping.items()) + [("surname", "Britva")]
    },
)
def from_dummy():
    pass


@writer(dump=lambda mapping: str(mapping))
def to_dummy():
    pass


def test_dummy_load():
    s = "name"
    assert _dummy_load(s) == {"value": s}


def test_dummy_dump():
    d = {"name": "Boris"}
    assert _dummy_dump(d) == str(d)


def test_dummy_pre_processing():
    d = {"name": "Boris"}
    assert _dummy_pre_processing(d) == d


def test_reader_example():
    assert from_dummy("Boris") == Config(
        {"name": "Boris", "surname": "Britva"}
    )


def test_writer_example():
    assert to_dummy({"name": "Boris"}) == str({"name": "Boris"})
