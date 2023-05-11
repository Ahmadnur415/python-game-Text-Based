from typing import TYPE_CHECKING, Tuple

from ..items.equipment import EquipmentSlots
from ..items.item import EquippableItem
from ..items.item.utils import WeaponsSkills
from ..items.skill import Skill

if TYPE_CHECKING:
    from . import Entity


def skills(self: "Entity") -> Tuple["Skill", ...]:
    currItem = None
    itemMainHand = self.equipment[EquipmentSlots.MAIN_HAND]
    itemOffHand = self.equipment[EquipmentSlots.OFF_HAND]
    itemTwoHand = self.equipment[EquipmentSlots.TWO_HAND]

    if itemMainHand:
        currItem = itemMainHand
    elif not itemMainHand and itemOffHand:
        currItem = itemOffHand
    elif itemTwoHand:
        currItem = itemTwoHand

    if not currItem:
        return (Skill("punch_0001"),)

    get_item = self.search_item(inv_id=currItem[0], item_id=currItem[1])

    if (
        not get_item
        or not isinstance(get_item.data, EquippableItem)
        or not get_item["skills"]
    ):
        return (Skill("punch_0001"),)


    addSkills = WeaponsSkills.get(get_item.data.sub_type, None)
    currSkills = list(get_item["skills"])

    if addSkills:
        for a in addSkills:
            currSkills.append(Skill(a))

    return currSkills
