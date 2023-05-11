from enum import Enum
from typing import Dict, NewType, Tuple, TypeVar

from ..equipment import EquipmentSlots

__all__ = (
    "ItemQuality",
    "ItemType",
    "ItemSubtypeConsumable",
    "ItemSubtypeEquippable",
    "SLOTEQUIP",
    "INV_ID",
    "ITEM_ID",
)


INV_ID = TypeVar("INV_ID")
ITEM_ID = TypeVar("ITEM_ID")


class ItemQuality(Enum):
    COMMON = 1
    UNCOMMON = 2
    RARE = 3
    EPIC = 4
    LEGENDARY = 5
    SPECIAL = 6


class ItemType(Enum):
    EQUIPPABLE = "EQUIPPABLE"
    CONSUMABLE = "CONSUMABLE"


class ItemSubtypeEquippable(Enum):
    HELMET = "HELMET"
    ARMOR = "ARMOR"
    SHOES = "SHOES"
    SWORD = "SWORD"
    BOW = "BOW"
    STAFF = "STAFF"
    DAGGER = "DAGGER"
    LONG_SWORD = "LONG SOWRD"


class ItemSubtypeConsumable(Enum):
    FOOD = "FOOD"
    POTION = "POTION"


SLOTEQUIP: Dict[ItemSubtypeEquippable, tuple[EquipmentSlots, ...]] = {
    ItemSubtypeEquippable.HELMET: (EquipmentSlots.HEAD,),
    ItemSubtypeEquippable.ARMOR: (EquipmentSlots.BODY,),
    ItemSubtypeEquippable.SHOES: (EquipmentSlots.FOOT,),
    ItemSubtypeEquippable.SWORD: (
        EquipmentSlots.MAIN_HAND,
        EquipmentSlots.OFF_HAND,
        EquipmentSlots.TWO_HAND,
    ),
    ItemSubtypeEquippable.LONG_SWORD: (EquipmentSlots.TWO_HAND,),
    ItemSubtypeEquippable.DAGGER: (EquipmentSlots.MAIN_HAND, EquipmentSlots.OFF_HAND),
    ItemSubtypeEquippable.BOW: (EquipmentSlots.TWO_HAND,),
    ItemSubtypeEquippable.STAFF: (EquipmentSlots.MAIN_HAND,),
}


WeaponsSkills: Dict[ItemSubtypeEquippable, Tuple[str, ...]] = {
    ItemSubtypeEquippable.SWORD: ("slash_0004",),
    ItemSubtypeEquippable.BOW: ("shoot_0005",),
    ItemSubtypeEquippable.LONG_SWORD: ("slash_0004",),
    ItemSubtypeEquippable.DAGGER: ("slash_0004",),
    ItemSubtypeEquippable.STAFF: ("fire_bolt_0006",),
}
