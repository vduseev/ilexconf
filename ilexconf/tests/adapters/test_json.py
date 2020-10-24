from ilexconf.tests.conftest import settings_json_dict, settings_json_file_path
import sys
import pytest
import pathlib


from ilexconf.adapters.json import from_json, to_json
from ilexconf.exceptions import UnsupportedDataSourceType, UnsupportedDataDestinationType


def test_empty_arguments():
    with pytest.raises(TypeError):
        from_json()
    with pytest.raises(TypeError):
        to_json()


def test_from_file_object(settings_json_file_path, settings_json_dict):
    with open(settings_json_file_path, "r") as f:
        config = from_json(f)

        assert config.as_dict() == settings_json_dict


def test_from_path_object(settings_json_file_path, settings_json_dict):
    p = pathlib.Path(settings_json_file_path)
    config = from_json(p)

    assert config.as_dict() == settings_json_dict


def test_from_json_string(settings_json_string, settings_json_dict):
    config = from_json(settings_json_string)

    assert config.as_dict() == settings_json_dict


def test_from_path_string(settings_json_file_path, settings_json_dict):
    config = from_json(str(settings_json_file_path))

    assert config.as_dict() == settings_json_dict


def test_from_wrong_argument():
    with pytest.raises(UnsupportedDataSourceType):
        from_json(1001)


def test_to_string(settings_json_dict, settings_json_string):
    strjson = to_json(settings_json_dict, indent=None)

    assert strjson == settings_json_string


def test_to_file_object(tmp_path, settings_json_dict):
    path = tmp_path / "save.json"
    with open(path, "w") as f:
        to_json(settings_json_dict, f)

    assert from_json(path).as_dict() == settings_json_dict


def test_to_stdout(capsys, settings_json_dict, settings_json_string):
    to_json(settings_json_dict, sys.stdout, indent=None)
    captured = capsys.readouterr()

    assert captured.out == settings_json_string


def test_to_path(tmp_path, settings_json_dict):
    path = pathlib.Path(tmp_path / "save.json")
    to_json(settings_json_dict, path)

    assert from_json(path).as_dict() == settings_json_dict


def test_to_string_path(tmp_path, settings_json_dict):
    path = str(tmp_path / "save.json")
    to_json(settings_json_dict, path)

    assert from_json(path).as_dict() == settings_json_dict


def test_to_wrong_argument(settings_json_dict):
    with pytest.raises(UnsupportedDataDestinationType):
        to_json(settings_json_dict, True)
