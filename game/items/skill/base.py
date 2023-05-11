from dataclasses import asdict
from typing import Optional, Union

from pydantic import Field, PositiveInt
from pydantic.dataclasses import dataclass

from ..effect import BaseEffect
from .utils import *


@dataclass
class BaseSkill:
    id: str
    name: str
    description: str
    description_of_being_used: str
    type_damage: TypeDamage
    damage: Union[PositiveInt, ModifierDamage]
    countdown: int = 0
    cost: Cost = Cost(mana=0, stamina=0)
    effect: Optional[BaseEffect] = None

    def dict(self):
        return asdict(self)
