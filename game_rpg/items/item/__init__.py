from typing import TYPE_CHECKING, Optional, Tuple, Union
from uuid import uuid4

from .base import BaseItem
from .consumable_item import ConsumableItem
from .equippable_item import EquippableItem

if TYPE_CHECKING:
    from ..skill import Skill

__all__ = ("Item", "BaseItem", "ConsumableItem", "EquippableItem")


class Item:
    def __init__(self, item_id: str, count: int = 1) -> None:
        self.item_id = item_id
        self.count = count

        self.__inventory_id = uuid4()
        self.__skills = tuple()

    def __getitem__(self, name: str):
        item = self.data

        if item is None:
            raise ValueError(f"Invalid item ID: {self.item_id}")
        if isinstance(item, EquippableItem) and name == "skills":
            return self.__get_skills()

        return getattr(item, name)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(inv_id={self.inventory_id}, item_id={self.item_id!r}, count={self.count})"

    def __get_skills(self) -> Optional[Tuple["Skill", ...]]:
        item = self.data
        if isinstance(item, ConsumableItem):
            return

        if not item.skills:
            return

        if self.__skills:
            return self.__skills

        from ..skill import Skill

        skills = []
        for skill_id in item.skills:
            skills.append(Skill(skill_id, str(self.__inventory_id)))

        self.__skills = tuple(skills)
        return self.__skills

    @property
    def count(self) -> int:
        """Mendapatkan jumlah item"""
        return self._amount if self["stackable"] else 1

    @count.setter
    def count(self, value: int):
        self._amount = value

    @property
    def inventory_id(self) -> str:
        return str(self.__inventory_id)

    @property
    def data(self) -> Union[EquippableItem, ConsumableItem]:
        from .db import get_item

        return get_item(id=self.item_id)
