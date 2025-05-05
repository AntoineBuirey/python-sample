import time
from datetime import timedelta, datetime
from cache import Cache
import pytest

def test_cache_expire_in_caches_result():
    calls = []

    @Cache(expire_in=timedelta(seconds=1))
    def add(a, b):
        calls.append((a, b))
        return a + b

    result1 = add(1, 2)
    result2 = add(1, 2)
    assert result1 == 3
    assert result2 == 3
    assert len(calls) == 1  # Only called once due to caching

def test_cache_expire_in_expires():
    calls = []

    @Cache(expire_in=timedelta(milliseconds=100))
    def mul(a, b):
        calls.append((a, b))
        return a * b

    result1 = mul(2, 3)
    time.sleep(0.15)
    result2 = mul(2, 3)
    assert result1 == 6
    assert result2 == 6
    assert len(calls) == 2  # Called twice due to expiration

def test_cache_with_kwargs():
    calls = []

    @Cache(expire_in=timedelta(seconds=1))
    def sub(a, b=0):
        calls.append((a, b))
        return a - b

    result1 = sub(5, b=2)
    result2 = sub(5, b=2)
    assert result1 == 3
    assert result2 == 3
    assert len(calls) == 1

def test_cache_expire_at():
    calls = []
    expire_at = datetime.now() + timedelta(milliseconds=100)

    @Cache(expire_at=expire_at)
    def div(a, b):
        calls.append((a, b))
        return a / b

    result1 = div(6, 2)
    result2 = div(6, 2)
    assert result1 == 3
    assert result2 == 3
    assert len(calls) == 1
    time.sleep(0.15)
    result3 = div(6, 2)
    assert result3 == 3
    assert len(calls) == 2


def test_cache_raises_if_no_expire():
    with pytest.raises(ValueError):
        @Cache()
        def foo(): pass # pragma: no cover

def test_cache_raises_if_both_expire():
    with pytest.raises(ValueError):
        @Cache(expire_in=timedelta(seconds=1), expire_at=datetime.now())
        def foo(): pass # pragma: no cover