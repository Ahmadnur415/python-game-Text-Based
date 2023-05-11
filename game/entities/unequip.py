from typing import TYPE_CHECKING, Literal, Union

from ..items.equipment import EquipmentSlots
from ..items.item import Item

if TYPE_CHECKING:
    from . import Entity


def unequip(self: "Entity", slot: "EquipmentSlots") -> Union["Item", Literal[False]]:
    """Methode untuk melepaskan equipment

    Args:
        slot (EquipmentSlots): Slot yang dipilih untuk melepaskan equipment

    """

    """mendapatkan `Inventory Id` dan `Item Id` dari equipment"""
    curr_slot = self.equipment.get(slot, None)
    if not curr_slot:
        return False
    inv_id, item_id = curr_slot

    """Mencari item di inventory dengan inv_id dan item_ud"""
    curr_item = None
    for item_in_inventory in self.inventory:
        if (
            inv_id == item_in_inventory.inventory_id
            and item_id == item_in_inventory.item_id
        ):
            curr_item = item_in_inventory
            break
    else:
        """Mengambil item di data base jika tidak ada di inventory"""
        curr_item = Item(item_id)

    self.equipment[slot] = None
    self.stats -= curr_item.data.stats
    return curr_item
