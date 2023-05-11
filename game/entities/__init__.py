from typing import Any, Dict, List, Mapping, Union

from ..items.equipment import Equipment, EquipmentSlots
from ..items.item import Item
from ..items.skill import SkillsCapacity
from . import (
    add_item,
    equip,
    extend_items,
    inventory_properties,
    remove_item,
    search_item,
    unequip,
)
from .entity_stats import EntityStats

__all__ = ("Entity",)


class Entity:
    def __init__(
        self,
        *,
        stats: Union["EntityStats", Mapping[str, Any]] = {},
        equipments: dict[Union["EquipmentSlots", str], Union["Item", str]] = {},
    ):
        """Membuat Object EntityStats"""
        if isinstance(stats, dict):
            stats = EntityStats(**stats)

        """Validasi stats"""
        if not isinstance(stats, EntityStats):
            raise ValueError("Error - Inisialisai stats error")

        self.stats = stats
        self.inventory: List[Item] = []
        self.equipment = Equipment()
        self.skills = SkillsCapacity(self)

        """inisialisasi Equipment"""
        for slot_equip, item_to_equip in equipments.items():
            if isinstance(slot_equip, str):
                slot_equip = EquipmentSlots(slot_equip)

            if isinstance(item_to_equip, str):
                item_to_equip = Item(item_to_equip)

            self.equip(item_to_equip, slot=slot_equip, force=True, append_to_inv=True)

        """inisialisasi stats dan level"""
        self["level"] = 1
        self["health"] = self["max_health"]
        self["mana"] = self["max_mana"]
        self["stamina"] = self["max_stamina"]

    @property
    def classname(self) -> str:
        return self.__class__.__name__

    def __getitem__(self, name: str) -> Any:
        return getattr(self.stats, name)

    def __setitem__(self, name: str, value: Any) -> None:
        if not hasattr(self.stats, name):
            raise TypeError(f"TIdak ada nama = {name}")
        setattr(self.stats, name, value)

    add_item = add_item.add_item
    extend_items = extend_items.extend_items
    equippable_items = inventory_properties.equippable_items
    consumable_items = inventory_properties.consumable_items
    remove_item = remove_item.remove_item
    equip = equip.equip
    unequip = unequip.unequip
    search_item = search_item.search_item
