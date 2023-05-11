from typing import TYPE_CHECKING, Any, Literal

from pydantic import Field
from pydantic.dataclasses import dataclass

from ...exceptions import EntityValuesFullError
from ...stats import ValueStats
from .base import BaseEffect

if TYPE_CHECKING:
    from ...entities import Entity


__all__ = ("Recovery", "Increase", "Decrease")


@dataclass
class Recovery(BaseEffect):
    stats: ValueStats
    name: Literal["Recovery"] = "Recovery"

    def apply(self, entity: "Entity", *, force: bool = False):
        """Menerapkan penyembuhan pada entity

        Args:
            entity (Entity): Target penyembuhan
            force (bool, optional): force jika stats full. Defaults to False.

        Raises:
            EntityValuesFullError: Full stats. Return stats yang full
        """

        stats = self.stats.dict(filter=True)
        if not force:
            """Cek stat jika full"""
            is_full = True
            for stat in stats.keys():
                if entity[stat] != entity[f"max_{stat}"]:
                    is_full = False
                    break

            if is_full:
                raise EntityValuesFullError(*tuple(stats.keys()))

        """ Apply effect """
        for stat, value in stats.items():
            entity[stat] += value

        return True


@dataclass
class Increase(BaseEffect):
    name: Literal["Increase"] = "Increase"

    def apply(self, entity: "Entity"):
        stats = self.stats.dict(filter=True)

        for stat, value in stats.items():
            entity[stat] += value

        return True


@dataclass
class Decrease(BaseEffect):
    name: Literal["Decrease"] = "Decrease"

    def apply(self, entity: "Entity"):
        stats = self.stats.dict(filter=True)

        for stat, value in stats.items():
            entity[stat] -= value

        return True


@dataclass
class StealDamage(BaseEffect):
    pass