from ilexconf import Config

# from ilexconf.tests.debug import debug

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

    empty_cfg = Config()
    empty_cfg["f1"] = False
    assert empty_cfg["f1"] is False
    empty_cfg["f2"]["g3"]["h3"] = 123
    assert empty_cfg["f2.g3.h3"] == 123
    empty_cfg["u1.u4.u6"] = True
    assert empty_cfg["u1"]["u4"]["u6"] is True


def test_setattr():
    cfg = Config(NESTED, MERGABLE)
    cfg.a1.b1.c1 = 8
    assert cfg.a1.b1.c1 == 8
