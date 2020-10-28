import pytest

from ilexconf.config import Config


def test_wrong_argument_type():
    config = Config()
    with pytest.raises(TypeError):
        config.update(1001)
