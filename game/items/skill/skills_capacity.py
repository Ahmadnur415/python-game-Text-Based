from typing import TYPE_CHECKING, Optional, Tuple

from ..equipment import EquipmentSlots

if TYPE_CHECKING:
    from ...entities import Entity
    from . import Skill


class SkillsCapacity:
    def __init__(self, entity: "Entity") -> None:
        self.__entity = entity

    def skills(self) -> Optional[Tuple["Skill", ...]]:
        skills = []
        entity = self.__entity
        currItem = None
        itemMainHand = entity.equipment[EquipmentSlots.MAIN_HAND]
        itemOffHand = entity.equipment[EquipmentSlots.OFF_HAND]
        itemTwoHand = entity.equipment[EquipmentSlots.TWO_HAND]

        if itemMainHand:
            currItem = itemMainHand
        elif not itemMainHand and itemOffHand:
            currItem = itemOffHand
        elif itemTwoHand:
            currItem = itemTwoHand

        """ Get Item Skill from current item """
        if currItem:
            item = entity.search_item(inv_id=currItem[0], item_id=currItem[1])
            if item and item["skills"]:
                return item["skills"]

        """Default skill"""
        return
