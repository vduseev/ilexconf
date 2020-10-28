import os
import pytest

from ilexconf.adapters.ini import from_ini, to_ini
from ilexconf.adapters.json import from_json, to_json


@pytest.fixture(scope="module", autouse=True)
def ini_dir(fixture_dir):
    return os.path.join(fixture_dir, "ini")
    

@pytest.fixture(scope="module", autouse=True)
def sample_ini(ini_dir):
    return os.path.join(ini_dir, "sample.ini")


def test_read_example(ini_dir, sample_ini):
    config = from_ini(sample_ini)

    json_counterpart_path = os.path.join(ini_dir, "sample.json")
    json_analogue = from_json(json_counterpart_path)
    json_analogue["bitbucket.org"].submerge(json_analogue["DEFAULT"])
    json_analogue["topsecret.server.com"].submerge(json_analogue["DEFAULT"])
    assert config == json_analogue


def test_write_example(sample_ini, tmp_path):
    config = from_ini(sample_ini)

    path = tmp_path / "sample.ini"
    to_ini(config, path)

    reloaded = from_ini(path)
    print(to_json(config))
    print(to_json(reloaded))
    assert config == reloaded
