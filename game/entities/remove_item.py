from typing import TYPE_CHECKING

from ..exceptions import CantRemoveItemError, ItemNotInInventoryError

if TYPE_CHECKING:
    from ..items.item import Item
    from . import Entity


def remove_item(self: "Entity", item: "Item"):
    """Menghapus item dari inventory

    Args:
        item (Item): object item yang akan dihapus

    Raises:
        CantRemoveItemError: Tidak dapat di hapus karena item sedang di pakai
        ItemNotInInventoryError: Item tidak ada dalam inventory
    """

    for _, equip_item in self.equipment.items():
        if (item.inventory_id, item.item_id) == equip_item:
            raise CantRemoveItemError("[Error] Item sedang di pakai")

    if item not in self.inventory:
        raise ItemNotInInventoryError(f"[Error] {item} tidak ada di inventroy")

    self.inventory.remove(item)
