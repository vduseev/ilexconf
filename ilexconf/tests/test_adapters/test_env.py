import os
import pytest

from ilexconf import Config, from_env, to_env

# from ilexconf.tests.debug import debug


def test_from_env_basic():
    os.environ["AWS_DEFAULT_REGION"] = "us-east-1"

    # Prefix = AWS_
    # Separator = __
    # Lowercase = True
    config = from_env(prefix="AWS_", separator="__", lowercase=True)
    assert config.as_dict() == {"default_region": "us-east-1"}

    # Prefix = "" (empty)
    # Separator = ""
    # Lowercasee = False (default)
    # TODO: Tell about environment variables dashes converted to underscores in docs
    config = from_env()
    assert config.AWS_DEFAULT_REGION == "us-east-1"


def test_from_env_no_prefix():
    os.environ["AWS_DEFAULT_REGION"] = "us-east-1"

    # debug()
    config = from_env(separator="_", lowercase=True)
    with pytest.raises(AssertionError):
        # Should raise error, because correct key is config.aws.deault.region
        assert config.default.region == "us-east-1"
    assert config.aws.default.region == "us-east-1"

    config = from_env(lowercase=True)
    assert config.aws_default_region == "us-east-1"

    config = from_env(prefix=None, lowercase=True)
    assert config.aws_default_region == "us-east-1"

    config = from_env()
    with pytest.raises(AssertionError):
        # Should raise error, because correct key is uppercase
        assert config.aws_default_region == "us-east-1"
    assert config.AWS_DEFAULT_REGION == "us-east-1"


def test_from_env_no_separator():
    os.environ["AWS_DEFAULT_REGION"] = "us-east-1"

    config = from_env(prefix="_", lowercase=True)
    with pytest.raises(AssertionError):
        assert config.aws_default_region == "whatever"
    assert config.aws_default_region == Config()

    # debug()
    config = from_env(separator="", lowercase=True)
    with pytest.raises(AssertionError):
        assert config.AWS_DEFAULT_REGION == "us-east-1"
    assert config.aws_default_region == "us-east-1"

    config = from_env(separator=None)
    with pytest.raises(AssertionError):
        assert config.aws_default_region == "us-east-1"
    assert config.AWS_DEFAULT_REGION == "us-east-1"

    config = from_env()
    with pytest.raises(AssertionError):
        assert config.aws_default_region == "us-east-1"
    assert config.AWS_DEFAULT_REGION == "us-east-1"


def test_from_env_one_dash_separator():
    os.environ["AWS_DEFAULT_REGION"] = "us-east-1"

    config = from_env(separator="_")
    with pytest.raises(AssertionError):
        assert config.aws.default.region == "us-east-1"
    assert config.AWS.DEFAULT.REGION == "us-east-1"

    config = from_env(separator="_", lowercase=True)
    with pytest.raises(AssertionError):
        assert config.AWS.DEFAULT.REGION == "us-east-1"
    assert config.aws.default.region == "us-east-1"


def test_to_env_current_context():
    # TODO: Implement
    pass

    os.environ["AWS_DEFAULT_REGION"] = "us-east-1"

    config = from_env(lowercase=True)
    config.aws_default_region = "us-east-2"
    to_env(config, prefix="", uppercase=True)
    assert os.environ["AWS_DEFAULT_REGION"] == "us-east-2"

    to_env(config, prefix="MY", lowercase=False)
    assert os.environ["MYaws_default_region"] == "us-east-2"

    to_env(config, prefix="mY_")
    assert os.environ["mY_aws_default_region"] == "us-east-2"

    to_env(config, prefix="MY_", uppercase=True)
    with pytest.raises(KeyError):
        # Should not exist because MY_ is prefix
        assert os.environ["MY__AWS_DEFAULT_REGION"] == "us-east-2"
    assert os.environ["MY_AWS_DEFAULT_REGION"] == "us-east-2"


def test_to_env_os_system():
    # TODO: Implement
    pass


def test_to_env_popen():
    # TODO: Implement
    pass


def test_to_env_fork():
    # TODO: Implement
    pass


def test_to_env_execv():
    # TODO: Implement
    pass
