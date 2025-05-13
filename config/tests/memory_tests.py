import pytest
from typing import Any
from config.config import MemoryConfig


@pytest.mark.parametrize(
    "initial, key, expected",
    [
        ({"foo": 123}, "foo", 123),
        ({"foo": "bar"}, "foo", "bar"),
        ({"foo": True}, "foo", True),
        ({"foo": 1.5}, "foo", 1.5),
        ({"foo": {"bar": 42}}, "foo.bar", 42),
        ({"foo": {"bar": {"baz": "qux"}}}, "foo.bar.baz", "qux"),
        ({"foo": "${bar}", "bar": 99}, "foo", "99"),
        ({"foo": "${bar}", "bar": "${baz}", "baz": 7}, "foo", "7"),
    ],
    ids=[
        "get_simple_int",
        "get_simple_str",
        "get_simple_bool",
        "get_simple_float",
        "get_nested",
        "get_deep_nested",
        "get_reference",
        "get_nested_reference",
    ]
)
def test_get_happy(initial, key, expected):
    # Arrange

    config = MemoryConfig(initial)

    # Act

    result = config.get(key)

    # Assert

    assert result == expected

@pytest.mark.parametrize(
    "initial, key, default, set_if_not_found, expected",
    [
        ({}, "foo", 42, False, 42),
        ({}, "foo", 42, True, 42),
        (None, "foo", 42, False, 42),
        (None, "foo", 42, True, 42),
    ],
    ids=["get_default_no_set", "get_default_and_set", "get_default_no_set_none", "get_default_and_set_none"]
)
def test_get_edge_cases(initial, key, default, set_if_not_found, expected):
    # Arrange

    config = MemoryConfig(initial)

    # Act & Assert

    if set_if_not_found:
        result = config.get(key, default=default, set_if_not_found=set_if_not_found)
        assert result == expected
        assert config.get(key) == default
    else:
        result = config.get(key, default=default, set_if_not_found=set_if_not_found)
        assert result == expected
        assert key not in config._config


@pytest.mark.parametrize(
    "initial, key, test_id",
    [
        ({}, "foo", "get_missing_no_default"),
        ({"foo": {"bar": {}}}, "foo.bar", "get_nonendpoint_dict_no_default"),
    ],
    ids=lambda p: p if isinstance(p, str) else None
)
def test_get_errors(initial, key, test_id):
    # Arrange

    config = MemoryConfig(initial)

    # Act & Assert

    with pytest.raises(KeyError):
        config.get(key)

@pytest.mark.parametrize(
    "initial, key, value, expected, test_id",
    [
        ({}, "foo", 123, 123, "set_simple"),
        ({}, "foo.bar", "baz", "baz", "set_nested"),
        ({"foo": {"bar": 1}}, "foo.bar", 2, 2, "set_overwrite"),
        ({}, "foo.bar.baz", 7, 7, "set_deep_nested"),
    ],
    ids=lambda p: p if isinstance(p, str) else None
)
def test_set_happy(initial, key, value, expected, test_id):
    # Arrange

    config = MemoryConfig(initial)

    # Act

    config.set(key, value)

    # Assert

    assert config.get(key) == expected

@pytest.mark.parametrize(
    "initial, key, value, test_id",
    [
        ({"foo": 1}, "foo.bar", "baz", "set_on_non_dict"),
    ],
    ids=["set_on_non_dict"]
)
def test_set_edge_cases(initial, key, value, test_id):
    # Arrange

    config = MemoryConfig(initial)

    # Act

    with pytest.raises(TypeError):
        config.set(key, value)


@pytest.mark.parametrize(
    "initial, key, test_id",
    [
        ({"foo": 1}, "foo", "remove_simple"),
        ({"foo": {"bar": 2}}, "foo.bar", "remove_nested"),
        ({"foo": {"bar": {"baz": 3}}}, "foo.bar.baz", "remove_deep_nested"),
    ],
    ids=["remove_simple", "remove_nested", "remove_deep_nested"]
)
def test_remove_happy(initial, key, test_id):
    # Arrange

    config = MemoryConfig(initial)

    # Act

    config.remove(key)

    # Assert

    assert key not in config._config

@pytest.mark.parametrize(
    "initial, key, test_id",
    [
        ({}, "foo", "remove_missing"),
        ({"foo": {"bar": 1}}, "bar.foo", "remove_missing_nested"),
        ({"foo": {"bar": 1}}, "foo.baz", "remove_missing_nested_2"),
        ({"foo": 1}, "foo.bar", "remove_on_non_dict"),
    ],
    ids=["remove_missing", "remove_missing_nested", "remove_missing_nested_2", "remove_on_non_dict"]
)
def test_remove_errors(initial, key, test_id):
    # Arrange

    config = MemoryConfig(initial)

    # Act & Assert

    with pytest.raises(KeyError):
        config.remove(key)


def test_set_reference():
    # Arrange

    config = MemoryConfig({
        "foo": "${bar}",
        "bar": 42,
        "baz" : {
            "qux": "${foo}",
            "value": 69
        },
        "test": "${baz.value}",
        "complex": "${baz.value}.01"
    })

    # Assert

    assert config.get("foo") == "42"
    assert config.get("bar") == 42
    assert config.get("baz.qux") == "42"
    assert config.get("test") == "69"
    assert config.get("complex") == "69.01"