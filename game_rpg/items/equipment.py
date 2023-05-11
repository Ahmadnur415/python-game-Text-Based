from enum import Enum
from typing import Dict, NewType, Optional, Tuple

INV_ID = NewType("INV_ID", str)
ITEM_ID = NewType("ITEM_ID", str)


class EquipmentSlots(Enum):
    MAIN_HAND = "MAIN HAND"
    OFF_HAND = "OFF HAND"
    TWO_HAND = "TWO HAND"

    HEAD = "HEAD"
    BODY = "BODY"
    FOOT = "FOOT"


def Equipment() -> Dict["EquipmentSlots", Optional[Tuple[INV_ID, ITEM_ID]]]:
    """Equipment

    Returns:
        Tuple[INV_ID, ITEM_ID]: inventory_id, item_id
    """
    return {EquipmentSlots(slot): None for slot in EquipmentSlots}
