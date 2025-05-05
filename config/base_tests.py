import pytest
from typing import Any
from config import BaseConfig


# Minimal concrete subclass for testing
class DummyConfig(BaseConfig):
    def __init__(self, initial=None):
        self._initial = initial or {}
        super().__init__()

    def _load(self):
        self._config = self._initial.copy()
        return self

    def _save(self):
        self._initial = self._config.copy()
        return self

    def _reload(self):
        # Simulate reload by reloading from _initial
        self._config = self._initial.copy()
        return self

@pytest.mark.parametrize(
    "initial, key, expected, test_id",
    [
        ({"foo": 123}, "foo", 123, "get_simple_int"),
        ({"foo": "bar"}, "foo", "bar", "get_simple_str"),
        ({"foo": True}, "foo", True, "get_simple_bool"),
        ({"foo": 1.5}, "foo", 1.5, "get_simple_float"),
        ({"foo": {"bar": 42}}, "foo.bar", 42, "get_nested"),
        ({"foo": {"bar": {"baz": "qux"}}}, "foo.bar.baz", "qux", "get_deep_nested"),
        ({"foo": "${bar}", "bar": 99}, "foo", "99", "get_reference"),
        ({"foo": "${bar}", "bar": "${baz}", "baz": 7}, "foo", "7", "get_nested_reference"),
    ],
    ids=lambda p: p if isinstance(p, str) else None
)
def test_get_happy(initial, key, expected, test_id):
    # Arrange

    config = DummyConfig(initial)

    # Act

    result = config.get(key)

    # Assert

    assert result == expected

@pytest.mark.parametrize(
    "initial, key, default, set_if_not_found, expected, test_id",
    [
        ({}, "foo", 42, False, 42, "get_default_no_set"),
        ({}, "foo", 42, True, 42, "get_default_and_set"),
    ],
    ids=["get_default_no_set", "get_default_and_set"]
)
def test_get_edge_cases(initial, key, default, set_if_not_found, expected, test_id):
    # Arrange

    config = DummyConfig(initial)

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

    config = DummyConfig(initial)

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

    config = DummyConfig(initial)

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

    config = DummyConfig(initial)

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

    config = DummyConfig(initial)

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

    config = DummyConfig(initial)

    # Act & Assert

    with pytest.raises(KeyError):
        config.remove(key)
