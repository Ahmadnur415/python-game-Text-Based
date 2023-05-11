from dataclasses import asdict
from typing import Any, Dict, Union

from pydantic.dataclasses import dataclass


@dataclass
class BaseStats:
    def __add__(self, other: Union["BaseStats", Dict[str, Any]]):
        if not isinstance(other, (BaseStats, dict)):
            raise TypeError("unsupported operand")

        for k, v in self:
            if isinstance(other, BaseStats):
                v += getattr(other, k, 0)

            elif isinstance(other, dict):
                v += other.get(k, 0)

            setattr(self, k, v)
        return self

    def __sub__(self, other: Union["BaseStats", Dict[str, Any]]):
        if not isinstance(other, (BaseStats, dict)):
            raise TypeError("unsupported operand")

        for k, v in self:
            if isinstance(other, BaseStats):
                v -= getattr(other, k, 0)

            elif isinstance(other, dict):
                v -= other.get(k, 0)

            setattr(self, k, v)
        return self

    def __iter__(self):
        return iter(self.dict().items())

    def __getitem__(self, name: str):
        return getattr(self, name)

    def __setitem__(self, name: str, value: int) -> None:
        setattr(self, name, value)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.dict(filter=True)})"

    def dict(self, *, filter: bool = False) -> Dict[str, Any]:
        data = asdict(self)
        if filter:
            data = {key: value for key, value in data.items() if value != 0}
        return data


@dataclass
class Stats(BaseStats):
    strength: int = 0
    dexterity: int = 0
    magic: int = 0
    perception: int = 0
    constitution: int = 0
    will: int = 0
    growth_hp: int = 0
    growth_mp: int = 0

    base_critical_change: float = 0.0
    base_critical_damage: float = 0.0

    base_health: int = 0
    base_mana: int = 0
    base_stamina: int = 0

    base_max_health: int = 0
    base_max_mana: int = 0
    base_max_stamina: int = 0

    base_defense: int = 0
    base_evasion: int = 0
    base_resistance: int = 0


@dataclass
class ValueStats(BaseStats):
    health: int = 0
    mana: int = 0
    stamina: int = 0
