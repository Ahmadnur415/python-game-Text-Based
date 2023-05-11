from typing import Any

from pydantic.dataclasses import dataclass

from ...stats import Stats

__all__ = ("BaseEffect",)


@dataclass
class BaseEffect:
    stats: Stats
    name: str

    def apply(self, *arg, **kwrgs) -> Any:
        ...
