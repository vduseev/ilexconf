from ilexconf import Config

import pytest


def test_simple_as_table(settings_json_dict):
    config = Config(settings_json_dict)
    headers, rows = config.as_table()

    assert headers == ["Setting", "Value"]
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
