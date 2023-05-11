from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from ..items.item import Item
    from . import Entity


def search_item(
    self: "Entity", *, inv_id: str, item_id: Optional[str] = None
) -> Optional["Item"]:
    for item_in_inventory in self.inventory:
        if inv_id == item_in_inventory.inventory_id:
            if item_id is None:
                return item_in_inventory

            if item_id == item_in_inventory.item_id:
                return item_in_inventory
    return None
