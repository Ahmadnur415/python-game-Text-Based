from typing import Union, Mapping

from ...stats import Stats, ValueStats
from ..effect import Increase, Recovery
from .consumable_item import ConsumableItem
from .equippable_item import EquippableItem
from .utils import *


def get_item(*, id: str) -> Union["EquippableItem", "ConsumableItem"]:
    return DB[id]


DB: Mapping[str, Union[EquippableItem, ConsumableItem]] = {
    "sword_0001": EquippableItem(
        **{
            "id": "sword_0001",
            "name": "Iron Sword",
            "price": 10,
            "quality": ItemQuality.COMMON,
            "sub_type": ItemSubtypeEquippable.SWORD,
            "description": "This is Sword",
            "in_shop": True,
            "skills": ("slab0003",),
            "stats": Stats(
                **{
                    "strength": 1,
                    "dexterity": 10,
                    "magic": 1,
                    "perception": 1,
                    "constitution": 1,
                    "will": 1,
                }
            ),
        }
    ),
    "bow_0002": EquippableItem(
        **{
            "id": "bow_0002",
            "name": "Bow",
            "price": 100,
            "quality": ItemQuality.UNCOMMON,
            "sub_type": ItemSubtypeEquippable.BOW,
            "description": "This is Bow",
            "in_shop": True,
            "stats": Stats(
                **{
                    "strength": 1,
                    "dexterity": 1,
                    "magic": 1,
                    "perception": 10,
                    "constitution": 1,
                    "will": 1,
                }
            ),
        }
    ),
    "staff_0003": EquippableItem(
        **{
            "id": "staff_0003",
            "name": "Staff",
            "price": 100,
            "quality": ItemQuality.RARE,
            "sub_type": ItemSubtypeEquippable.STAFF,
            "description": "This is Bow",
            "in_shop": True,
            "stats": Stats(
                **{
                    "strength": 1,
                    "dexterity": 1,
                    "magic": 1,
                    "perception": 10,
                    "constitution": 1,
                    "will": 1,
                }
            ),
        }
    ),
    "food_0004": ConsumableItem(
        **{
            "id": "food_0004",
            "name": "Food 0004",
            "price": 100,
            "quality": ItemQuality.LEGENDARY,
            "sub_type": ItemSubtypeConsumable.FOOD,
            "description": "This Food 0004",
            "in_shop": True,
            "effect": Increase(
                Stats(
                    **{
                        "strength": 1,
                        "dexterity": 1,
                        "magic": 1,
                        "perception": 10,
                        "constitution": 1,
                        "will": 1,
                    }
                )
            ),
        }
    ),
    "potion_0005": ConsumableItem(
        **{
            "id": "potion_0005",
            "name": "Potion 0005",
            "price": 1000,
            "quality": ItemQuality.SPECIAL,
            "sub_type": ItemSubtypeConsumable.POTION,
            "description": "This Potion 0005",
            "in_shop": True,
            "effect": Recovery(
                ValueStats(**{"health": 100, "mana": 100, "stamina": 100})
            ),
        }
    ),
    "sword_wood_0006": EquippableItem(
        **{
            "id": "sowrd_wood_0001",
            "name": "Sword Wood",
            "price": 100,
            "quality": ItemQuality.RARE,
            "sub_type": ItemSubtypeEquippable.SWORD,
            "description": "This is sword wood",
            "in_shop": True,
            "stats": {
                "strength": 10,
                "dexterity": 0,
                "magic": 11,
                "perception": 12,
                "constitution": 14,
                "will": 11,
            },
        }
    ),
}
