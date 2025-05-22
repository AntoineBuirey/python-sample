from singleton.singleton.singleton import Singleton
import pytest


@pytest.mark.parametrize(
    "args, kwargs",
    [
        ((), {}),
        ((1,), {}),
        (("foo", 42), {}),
        ((), {"a": 1},),
        ((1, 2), {"a": 3, "b": 4}),
    ],
    ids = ["no_args", "single_arg", "multiple_args", "no_args_with_kwargs", "multiple_args_with_kwargs"]
)
def test_singleton_instance_uniqueness(args, kwargs):
    # Arrange

    # Act
    instance1 = Singleton(*args, **kwargs)
    instance2 = Singleton(*args, **kwargs)

    # Assert
    assert instance1 is instance2
    assert isinstance(instance1, Singleton)
    assert isinstance(instance2, Singleton)

def test_singleton_instance_is_singleton_across_different_args():
    # Arrange

    # Act
    instance1 = Singleton(1, 2, a=3)
    instance2 = Singleton("foo", bar="baz")

    # Assert
    assert instance1 is instance2

def test_singleton_instance_is_singleton_across_no_args_and_args():
    # Arrange

    # Act
    instance1 = Singleton()
    instance2 = Singleton(123)
    instance3 = Singleton(a="b")

    # Assert
    assert instance1 is instance2
    assert instance2 is instance3


def test_singleton_instance_is_not_none():
    # Arrange

    # Act
    instance = Singleton()

    # Assert
    assert instance is not None

def test_singleton_instance_reset_for_test(monkeypatch):
    # Arrange
    monkeypatch.setattr(Singleton, "_Singleton__instance", None)

    # Act
    instance1 = Singleton()
    instance2 = Singleton()

    # Assert
    assert instance1 is instance2
    assert Singleton._Singleton__instance is instance1

@pytest.mark.parametrize(
    "pre_existing_instance, expected_new_instance",
    [
        (None, True),
        ("dummy", False),
    ],
    ids=["no_pre_existing_instance", "pre_existing_instance"]
)
def test_singleton_new_branch_coverage(monkeypatch, pre_existing_instance, expected_new_instance):
    # Arrange
    monkeypatch.setattr(Singleton, "_Singleton__instance", pre_existing_instance)

    # Act
    instance = Singleton()

    # Assert
    if expected_new_instance:
        assert isinstance(instance, Singleton)
    else:
        assert instance == pre_existing_instance

def test_singleton_direct_class_attribute_access():
    # Arrange

    # Act
    instance = Singleton()
    class_instance = Singleton._Singleton__instance

    # Assert
    assert instance is class_instance
