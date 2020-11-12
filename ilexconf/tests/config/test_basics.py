from ilexconf import Config

import pytest


NESTED = {
    "a1": {
        "b1": {"c1": 1, "C2": 2, "c3": 3},
        "b2": {"c1": "a", "c2": True, "c3": 1.1},
    },
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
    assert dict(cfg) == {"c1": 1, "C2": 2, "c3": "val"}


def test_nested_merge():
    cfg = Config(NESTED, MERGABLE)
    # "val" has replaced 3 as value for a1.b1.c3
    assert cfg.a1.b1.c3 == "val"
    # other values are still intact
    assert cfg.a1.b2.c3 == 1.1
    assert cfg.a1.b1.c1 == 1


def test_list():
    cfg = Config(WITH_LISTS)
    assert dict(cfg) == WITH_LISTS


def test_as_dict():
    cfg = Config(NESTED, MERGABLE)
    d = dict(cfg)
    assert d == MERGED


def test_setitem():
    cfg = Config(NESTED, MERGABLE)
    cfg["a1"]["b1"]["c1"] = 6
    assert cfg["a1"]["b1"]["c1"] == 6
    assert cfg.a1.b1.c1 == 6

    cfg = Config()
    cfg["f1"] = False
    assert cfg["f1"] is False

    cfg["f2"]["g3"]["h3"] = 123
    assert cfg["f2.g3.h3"] == 123

    cfg["u1.u4.u6"] = True
    assert cfg["u1"]["u4"]["u6"] is True


def test_setattr():
    cfg = Config(NESTED, MERGABLE)
    cfg.a1.b1.c1 = 8
    assert cfg.a1.b1.c1 == 8


def test_setattr_dict():
    d = {"b": True, "c": {"d": "thename"}}
    cfg = Config()

    # Assign dict to the key. It should atuomatically
    # get transformed into the Config object.
    cfg.a = d
    assert dict(cfg.a) == d
    assert cfg.a == Config(d)

    # Notice how the dict got transformed into a Config
    # during assignment so that now we have all the "nice"
    # accessibility features of Config.
    assert cfg.a.c.d == "thename"


def test_setattr_list_with_dict():
    l = [{"b": True, "c": {"d": "thename"}}, "somestring", True]
    cfg = Config()

    # When we assign a list to the key
    # it remains an instance of list, or
    # whatever sequence type it was.
    cfg.a = l
    assert isinstance(cfg.a, list)

    # Internally though any Mapping objects
    # inside that list, no matter how nested,
    # got transformed into the Config objects.
    assert cfg.a == [
        Config({"b": True, "c": {"d": "thename"}}),
        "somestring",
        True,
    ]

    # And, again, we get all the nice accessibility
    # shenenigans as a result of such transformation.
    assert cfg.a[0].c.d == "thename"


def test_lower():
    config = Config()

    config.merge({"SOME_KeY": "VALuE"})
    assert config.SOME_KeY == "VALuE"
    with pytest.raises(AssertionError):
        assert config.some_key == "VALuE"

    config.clear()
    config.merge({"SOME_KeY": "VALuE"})
    config = config.lower()

    assert config.some_key == "VALuE"
    with pytest.raises(AssertionError):
        assert config.SOME_KeY == "VALuE"


def test_upper():
    config = Config()

    config.merge({"sOmE_kEy": True})
    assert config.sOmE_kEy == True

    uppered = config.upper()
    assert uppered.SOME_KEY == True

    config.upper(inplace=True)
    assert config.SOME_KEY == True
