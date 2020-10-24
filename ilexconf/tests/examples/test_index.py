import pytest


def test_features():
    from ilexconf import Config
    config = Config()

    config.a.b.c = True

    assert (
        config.a.b.c == True
    )
    assert (
        config["a"]["b"]["c"] == True
    )
    assert (
        config["a.b.c"] == True
    )
    assert (
        config["a.b"].c == True
    )
    assert (
        config.a["b.c"] == True
    )
    assert (
        config.a["b"].c == True
    )

    if True:
        config.a.b.c = [
            "my_string",
            {"d": "nested_value"}
        ]

    assert (
        config.a.b.c[0] == "my_string"
    )
    assert (
        config.a.b.c[1] == Config({"d": "nested_value"})
    )
    assert (
        config.a.b.c[1].as_dict() == {"d": "nested_value"}
    )
