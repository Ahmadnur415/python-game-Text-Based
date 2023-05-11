from typing import Dict

from .base import BaseSkill
from .utils import Cost, ModifierDamage, TypeDamage


def get_skill(*, id: str):
    return DB[id]


DB: Dict[str, BaseSkill] = {
    "punch_0001": BaseSkill(
        id="Punch0001",
        name="Basic Punch",
        description="Ini adalah Sebuah Pukulan",
        description_of_being_used="Hit",
        type_damage=TypeDamage.PHYSICAL,
        damage=ModifierDamage(base=10, value=1, equal="self.level"),
    ),
    "hard_punch_0002": BaseSkill(
        id="hard_punch0002",
        name="Punch",
        description="Ini adalah sebuah pukulan keras",
        description_of_being_used="hit",
        countdown=2,
        type_damage=TypeDamage.PHYSICAL,
        damage=ModifierDamage(base=20, value=2, equal="self.level"),
        cost=Cost(mana=0, stamina=20),
    ),
    "slab_0003": BaseSkill(
        id="hard_punch0002",
        name="Punch",
        description="Ini adalah sebuah pukulan keras",
        description_of_being_used="hit",
        countdown=2,
        type_damage=TypeDamage.PHYSICAL,
        damage=ModifierDamage(base=20, value=2, equal="self.level"),
        cost=Cost(mana=0, stamina=20),
    ),
    "slash_0004": BaseSkill(
        id="slash_004",
        name="Slash",
        description="Ini adalah slash untuk sword",
        description_of_being_used="hit",
        type_damage=TypeDamage.PHYSICAL,
        damage=ModifierDamage(base=10, value=15, equal="self.strength", percent=True),
    ),
    "shoot_0005": BaseSkill(
        id="shoot_0005",
        name="Shoot",
        description="Ini adalah attack untuk bow",
        description_of_being_used="hit",
        type_damage=TypeDamage.PHYSICAL,
        damage=ModifierDamage(base=10, value=15, equal="self.perception", percent=True),
    ),
    "fire_bolt_0006": BaseSkill(
        id="fire_bolt_0006",
        name="Fire Bolt",
        description="Ini adalah attack untuk staff",
        description_of_being_used="hit",
        type_damage=TypeDamage.MAGIC,
        damage=ModifierDamage(base=10, value=15, equal="self.magic", percent=True),
    ),
}
