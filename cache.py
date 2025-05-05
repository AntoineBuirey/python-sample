#pylint: disable=too-few-public-methods, line-too-long

"""
A simple decorator to cache the result of a function for a specified amount of time.
This is useful for expensive computations or I/O-bound operations that don't change often.
"""

from datetime import datetime, timedelta
from typing import Callable, Any, TypeVar, Dict, Tuple, FrozenSet
from gamuLogger import Logger

Logger.set_module("cache")

T = TypeVar('T', bound=Callable[..., Any])

class Cache:
    """
    A simple decorator to cache the result of a function for a specified amount of time.
    """
    def __init__(self, /, expire_in: timedelta|None = None, expire_at: datetime|None = None) -> None:
        if expire_in is None and expire_at is None:
            raise ValueError("Either expire_in or expire_at must be provided")
        if expire_in is not None and expire_at is not None:
            raise ValueError("Only one of expire_in or expire_at can be provided")

        if expire_at is None:
            self.expire_in = expire_in
        elif expire_in is None:
            self.expire_in = expire_at - datetime.now()

        self.cache: Dict[
            Tuple[Tuple[Any, ...], FrozenSet[Tuple[Any, Any]]],  # Explicitly define frozenset type
            Tuple[Any, datetime]  # Result and timestamp
        ] = {}

    def __call__(self, func : Callable[..., T]) -> Callable[..., T]:
        def wrapper(*args : Any, **kwargs : Any) -> T:
            key = (args, frozenset(kwargs.items()))
            if key in self.cache:
                result, timestamp = self.cache[key]
                if datetime.now() - timestamp < self.expire_in:
                    Logger.trace(f"Using cached result for {func.__name__} with args {args} and kwargs {kwargs}")
                    return result
            Logger.trace(f"Cache miss for {func.__name__} with args {args} and kwargs {kwargs}")
            result = func(*args, **kwargs)
            self.cache[key] = (result, datetime.now())
            return result
        return wrapper
