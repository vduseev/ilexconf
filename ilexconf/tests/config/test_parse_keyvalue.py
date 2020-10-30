import pytest
from ilexconf.config import Config


key = "AWS_DEFAULT_REGION"
value = "us-east-1"


def test_example():
    assert Config.from_keyvalue(key, value) == Config({
        key: value
    })


def test_prefix_example():
    assert Config.from_keyvalue(key, value, prefix="AWS_") == Config({
        "DEFAULT_REGION": value
    })

    assert Config.from_keyvalue(key, value, prefix="AWS") == Config({
        "_DEFAULT_REGION": value
    })


def test_surrounded_by_separator():
    key = "AWS__DEFAULT_REGION__"
    assert Config.from_keyvalue(key, value, prefix="AWS") == Config({
        "DEFAULT_REGION": value
    })


def test_nested_example():
    assert Config.from_keyvalue(key, value, sep="_") == Config({
        "AWS": {
            "DEFAULT": {
                "REGION": value
            }
        }
    })

    assert Config.from_keyvalue(key, value, prefix="AWS", sep="_") == Config({
        "DEFAULT": {
            "REGION": value
        }
    })


def test_lower_example():
    assert Config.from_keyvalue(key, value, lowercase=True) == Config({
        key.lower(): value
    })


def test_upper_example():
    assert Config.from_keyvalue(key, value, uppercase=True) == Config({
        key.upper(): value
    })


def test_lower_and_upper():
    assert Config.from_keyvalue(key, value, lowercase=True, uppercase=True) == Config({
        key.lower(): value
    })


def test_empty_key():
    assert Config.from_keyvalue("", value) == Config({
        "": value
    })


def test_non_str_key():
    assert Config.from_keyvalue((1, 2), value) == Config({
        (1, 2): value
    })
