from typing import TYPE_CHECKING

from ..exceptions import IlegalEquipItemError, ItemAlreadyUsedError
from ..items.equipment import EquipmentSlots
from ..items.item import EquippableItem, Item

if TYPE_CHECKING:
    from . import Entity


def equip(
    self: "Entity",
    item: "Item",
    slot: "EquipmentSlots",
    *,
    force: bool = False,
    append_to_inv: bool = False
):
    """Methode untuk melengkapi item

    Args:
        item (Item): item yang akan di lengkapi
        slot (EquipmentSlots): lokasi item
        force (bool): Memaksa untuk melangkapi item. Default to False
        append_to_inv (bool): memasukkan item ke dalam inventory. Default to False
    """

    if not isinstance(item.data, EquippableItem):
        raise IlegalEquipItemError("Error - Tidak Bisa Dipakai")

    """raise jika item sudah terpakai"""
    if (item.inventory_id, item.item_id) in self.equipment.values() and not force:
        raise ItemAlreadyUsedError("Error - Item telah terpakai")

    """Mendapatkan item yang dipakai saat ini"""
    curr_item = self.equipment[slot]
    curr_item_main_hand = self.equipment[EquipmentSlots.MAIN_HAND]
    curr_item_off_hand = self.equipment[EquipmentSlots.OFF_HAND]
    curr_item_two_hand = self.equipment[EquipmentSlots.TWO_HAND]

    """tidak dapat melengkapi item karena item di slot lain sedang digunakan.
    tetapi masih dapat digunakan dengan menambahkan parm `force`
    """
    if curr_item:
        if not force:
            raise ItemAlreadyUsedError("Error - item di {slot}, sudah ada")
        self.unequip(slot)

    """Memvalidasi item yang akan dipakai di `TWO_HAND`"""
    if (curr_item_main_hand or curr_item_off_hand) and slot == EquipmentSlots.TWO_HAND:
        if not force:
            raise IlegalEquipItemError(
                "[Error] : Item tidak dapat di pakai. Terjadi konflik"
            )

        self.unequip(EquipmentSlots.MAIN_HAND)
        self.unequip(EquipmentSlots.OFF_HAND)

    """Memvalidasi item yang akan dipakai di `MAIN_HAND` atau `OFF_HAND`"""
    if (
        slot in (EquipmentSlots.MAIN_HAND, EquipmentSlots.OFF_HAND)
        and curr_item_two_hand
    ):
        if not force:
            raise IlegalEquipItemError(
                "[Error] : Item tidak dapat di pakai. Terjadi konflik. 2"
            )

        self.unequip(EquipmentSlots.TWO_HAND)

    """Menaruh informasi id_item dan inventory_id di equipment"""
    self.equipment[slot] = (item.inventory_id, item.item_id)
    self.stats += item.data.stats
    if append_to_inv and item not in self.inventory:
        self.inventory.append(item)

    return True
