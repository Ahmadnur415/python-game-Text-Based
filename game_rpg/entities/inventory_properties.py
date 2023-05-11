from typing import TYPE_CHECKING, Tuple

from ..items.item.utils import ItemType

if TYPE_CHECKING:
    from ..items.item import ConsumableItem, EquippableItem
    from . import Entity


@property
def equippable_items(self: "Entity") -> Tuple["EquippableItem"]:
    """Filter inventory hanya item equippable saja"""

    equippable = []
    for item in self.inventory:
        if item.data.type == ItemType.EQUIPPABLE:
            equippable.append(item)
    return tuple(equippable)


@property
def consumable_items(self: "Entity") -> Tuple["ConsumableItem"]:
    """Filter inventory hanya item consumable saja"""

    consumable = []
    for item in self.inventory:
        if item.data.type == ItemType.CONSUMABLE:
            consumable.append(item)
    return tuple(consumable)
