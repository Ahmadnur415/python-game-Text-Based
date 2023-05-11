from typing import Optional, Tuple

from pydantic.dataclasses import dataclass

from ...stats import Stats
from .base import BaseItem
from .utils import SLOTEQUIP, ItemSubtypeEquippable, ItemType


@dataclass
class EquippableItem(BaseItem):
    stats: Stats
    sub_type: ItemSubtypeEquippable
    skills: Optional[Tuple[str]] = None

    @property
    def type(self) -> "ItemType":
        return ItemType.EQUIPPABLE

    @property
    def slots_equip(self):
        return SLOTEQUIP[self.sub_type]

    @property
    def stackable(self):
        return False
