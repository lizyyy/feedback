"""In-process memoisation for expensive pure helpers.

The cache lives in a module-level dict and dies with the worker process; nothing here is
written down or compared against another process.
"""

from __future__ import annotations

from typing import Any, Callable

_CACHE: dict[int, Any] = {}


def memo_key(*args: Any, **kwargs: Any) -> int:
    """Key of a call in the in-process cache."""
    return hash((args, frozenset(kwargs.items())))


def memoize(func: Callable) -> Callable:
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        key = memo_key(func.__qualname__, *args, **kwargs)
        if key not in _CACHE:
            _CACHE[key] = func(*args, **kwargs)
        return _CACHE[key]

    wrapper.cache_clear = _CACHE.clear  # type: ignore[attr-defined]
    return wrapper
