from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..items.item import Item
    from . import Entity


def add_item(self: "Entity", item: "Item"):
    """Menambahkan item ke inventory

    Args:
        item (Item): Item yang ingin di tambahkan
    """

    if not item.data.stackable or not self.inventory:
        self.inventory.append(item)
        return

    for existing_item in self.inventory:
        if existing_item.item_id == item.item_id:
            existing_item.count += item.count
            break
    else:
        self.inventory.append(item)
