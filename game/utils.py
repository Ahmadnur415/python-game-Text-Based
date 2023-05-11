from typing import TypeVar

__all__ = ("clamp",)


_T = TypeVar("_T", int, float)


def clamp(x: _T, _min_x: _T, _max_x: _T) -> _T:
    return max(_min_x, min(x, _max_x))
