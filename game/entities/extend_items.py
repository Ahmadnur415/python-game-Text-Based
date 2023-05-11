from typing import TYPE_CHECKING, Iterable

if TYPE_CHECKING:
    from ..items.item import Item
    from . import Entity


def extend_items(self: "Entity", items: Iterable["Item"]):
    """Extend inventoey dengan menambahkan item dari Iterable"""
    for item in items:
        self.add_item(item)
