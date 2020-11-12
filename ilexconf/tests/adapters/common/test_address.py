import sys
from pathlib import Path

from ilexconf.adapters.common.address import Address


def test_read_stream(settings_json_file_path, settings_json_string):
    with open(settings_json_file_path, "rt") as f:
        assert Address.read(f) == settings_json_string


def test_read_string(settings_json_string):
    assert Address.read(settings_json_string) == settings_json_string


def test_read_string_path(settings_json_file_path, settings_json_string):
    assert (
        Address.read(
            settings_json_file_path, str_resolver=lambda string: True
        )
        == settings_json_string
    )


def test_read_path(settings_json_file_path, settings_json_string):
    path = Path(settings_json_file_path)
    assert Address.read(path) == settings_json_string


def test_write_stream(settings_json_string, capsys):
    Address.write(settings_json_string, sys.stdout)
    captured = capsys.readouterr()
    assert captured.out == settings_json_string


def test_write_file(settings_json_string, tmp_path):
    path = tmp_path / "save_file.txt"
    with open(path, "w") as f:
        Address.write(settings_json_string, f)

    with open(path, "r") as f:
        assert f.read() == settings_json_string


def test_write_string(settings_json_string):
    assert Address.write(settings_json_string) == settings_json_string


def test_write_string_path(settings_json_string, tmp_path):
    path = tmp_path / "save_string_path.txt"
    Address.write(
        settings_json_string, str(path), str_resolver=lambda string: True
    )

    with open(str(path), "rt") as f:
        assert f.read() == settings_json_string


def test_write_path(settings_json_file_path, settings_json_string, tmp_path):
    path = Path(tmp_path / "save_path.txt")
    Address.write(settings_json_string, path)

    with path.open("rt") as f:
        assert f.read() == settings_json_string
