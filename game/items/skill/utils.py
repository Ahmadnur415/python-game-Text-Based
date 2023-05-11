from enum import Enum
from typing import TYPE_CHECKING, Literal, Union

from pydantic import Field, PositiveFloat, PositiveInt
from pydantic.dataclasses import dataclass

if TYPE_CHECKING:
    from ...entities import Entity


__all__ = ("DAMAGE", "TypeDamage", "Cost", "ModifierDamage")


@dataclass
class Cost:
    mana: int = Field(0, ge=0)
    stamina: int = Field(0, ge=0)


@dataclass
class ModifierDamage:
    base: PositiveInt
    value: PositiveFloat
    equal: Union[str, PositiveFloat, None] = None
    percent: bool = False

    def get_damage(self, entity: "Entity", **kwrg):
        value = self.value
        if self.percent:
            value /= 100

        if self.equal:
            equal = round(self._get_equal(entity, **kwrg), 2)
            equal *= value
            return self.base + equal

        return self.base * value

    def _get_equal(self, entity: "Entity", **kwgs) -> PositiveFloat:
        """
        (base) + Equal * (value  ( / 100 if percent))
        (Base) * value / 100
        """

        if not self.equal:
            return 0

        if isinstance(self.equal, (int, float)):
            return self.equal

        by, key = self.equal.split(".")

        if by == "enemy" and not kwgs.get("enemy"):
            raise KeyError("Error : Requirement Enemy to get value ")

        # NOTE: Masih dalam pengembangan

        if by == "enemy":
            return kwgs["enemy"][key]
        else:
            return entity[key]


DAMAGE = Union[PositiveFloat, ModifierDamage]


class TypeDamage(Enum):
    PHYSICAL = "PHYSICAL"
    MAGIC = "MAGIC"
