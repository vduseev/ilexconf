from ilexconf import Config

import json
import pytest


NESTED = {
    "a1": {"b1": {"c1": 1, "C2": 2, "c3": 3}, "b2": {"c1": "a", "c2": True, "c3": 1.1}},
    "d1": False,
}

MERGABLE = {"a1": {"b1": {"c3": "val"}}}

MERGED = {
    "a1": {
        "b1": {"c1": 1, "C2": 2, "c3": "val"},
        "b2": {"c1": "a", "c2": True, "c3": 1.1},
    },
    "d1": False,
}

WITH_LISTS = {
    "database": {
        "connections": [
            {"host": "1.2.3.4", "port": 5000},
            {"host": "4.5.6.7", "port": 8080},
        ],
        "params": [["kw1", "kw2", 3], {"key": "value of key"}],
    }
}


def test_empty_config():
    cfg = Config()
    assert cfg == {}
    assert "a0" not in cfg


def test_nested_access():
    cfg = Config(NESTED)
    # Plain access
    assert cfg["a1"]["b1"]["c1"] == 1
    assert cfg["a1.b1.c1"] == 1
    assert cfg.a1.b1.c1 == 1
    # Mixed access
    assert cfg["a1"].b1.C2 == 2
    assert cfg.a1["b1"].c3 == 3
    assert cfg.a1.b2["c3"] == 1.1
    # Direct access
    assert cfg.d1 is False
    assert cfg["d1"] is False


def test_simple_merge():
    cfg = Config(Config({"c1": 1, "C2": 2, "c3": 3}), Config({"c3": "val"}))
    assert cfg.as_dict() == {"c1": 1, "C2": 2, "c3": "val"}


def test_nested_merge():
    cfg = Config(NESTED, MERGABLE)
    # "val" has replaced 3 as value for a1.b1.c3
    assert cfg.a1.b1.c3 == "val"
    # other values are still intact
    assert cfg.a1.b2.c3 == 1.1
    assert cfg.a1.b1.c1 == 1


def test_list():
    cfg = Config(WITH_LISTS)
    print(cfg)
    assert cfg.as_dict() == WITH_LISTS


def test_as_dict():
    cfg = Config(NESTED, MERGABLE)
    d = cfg.as_dict()
    assert d == MERGED


def test_setitem():
    cfg = Config(NESTED, MERGABLE)
    cfg["a1"]["b1"]["c1"] = 6
    assert cfg["a1"]["b1"]["c1"] == 6
    assert cfg.a1.b1.c1 == 6

    cfg = Config()
    cfg["f1"] = False
    assert cfg["f1"] is False

    #from .debug import debug
    #debug()
    cfg["f2"]["g3"]["h3"] = 123
    assert cfg["f2.g3.h3"] == 123

    cfg["u1.u4.u6"] = True
    assert cfg["u1"]["u4"]["u6"] is True


def test_setattr():
    cfg = Config(NESTED, MERGABLE)
    cfg.a1.b1.c1 = 8
    assert cfg.a1.b1.c1 == 8


def test_simple_as_table(settings_json_dict):
    config = Config(settings_json_dict)
    headers, rows = config.as_table()

    assert headers == ["Key", "Value"]
    assert rows == [
        ["database", ""],
        ["  connection", ""],
        ["    host", "localhost"],
        ["    port", "5432"],
    ]


def test_limit_as_table(settings_json_dict):
    config = Config(settings_json_dict)
    headers, rows = config.as_table(limit=3)

    assert rows == [
        ["database", ""],
        ["  connection", ""],
        ["    host", "localhost"],
        ["...", "..."],
    ]


def test_simple_flatten(settings_json_dict):
    config = Config(settings_json_dict)

    flat = config.flatten()
    assert flat == {
        "database.connection.host": "localhost",
        "database.connection.port": 5432,
    }


def test_list_flatten():
    # TODO: implement
    pass


def test_copy(settings_json_dict):
    config = Config(settings_json_dict)

    copy = config.copy()

    # Change value in initial object and check it
    config.database.connection.host = "1.2.3.4"
    assert config.database.connection.host == "1.2.3.4"

    # Make sure value in copied object has not changed
    assert copy.database.connection.host == "localhost"
