from importlib import reload
import os
import sys
import pytest

import ilexconf.adapters.yaml
from ilexconf.adapters.yaml import from_yaml, to_yaml
from ilexconf.adapters.json import from_json


@pytest.fixture(scope="module", autouse=True)
def yamldir(fixture_dir):
    return os.path.join(fixture_dir, "yaml")


def test_read_example(yamldir):

    from ilexconf.adapters.yaml import from_yaml, to_yaml

    config = from_yaml(os.path.join(yamldir, "simple.yaml"))

    json_counterpart_path = os.path.join(yamldir, "simple.json")
    json_analogue = from_json(json_counterpart_path)
    assert config == json_analogue


def test_write_example(yamldir, tmp_path):

    from ilexconf.adapters.yaml import from_yaml, to_yaml

    config = from_yaml(os.path.join(yamldir, "simple.yaml"))

    path = tmp_path / "simple.yaml"
    # import ilexconf.tests.debug
    to_yaml(config, path)

    reloaded = from_yaml(path)
    assert config == reloaded


def test_pyyaml(yamldir, monkeypatch, tmp_path):

    monkeypatch.setenv("_pytest_yaml_test_pyyaml", "true")
    import importlib

    importlib.reload(ilexconf.adapters.yaml)
    config = ilexconf.adapters.yaml.from_yaml(
        os.path.join(yamldir, "simple.yaml")
    )

    json_counterpart_path = os.path.join(yamldir, "simple.json")
    json_analogue = from_json(json_counterpart_path)
    assert config == json_analogue

    path = tmp_path / "simple-pyyaml.yaml"
    ilexconf.adapters.yaml.to_yaml(config, path)

    reloaded = ilexconf.adapters.yaml.from_yaml(path)
    assert config == reloaded


def test_noyaml(yamldir, monkeypatch):
    monkeypatch.setenv("_pytest_yaml_test_pyyaml", "true")
    monkeypatch.setenv("_pytest_yaml_test_noyaml", "true")
    import importlib

    importlib.reload(ilexconf.adapters.yaml)

    with pytest.raises(NotImplementedError):
        ilexconf.adapters.yaml.from_yaml(os.path.join(yamldir, "simple.yaml"))

    with pytest.raises(NotImplementedError):
        ilexconf.adapters.yaml.to_yaml("somepath")
