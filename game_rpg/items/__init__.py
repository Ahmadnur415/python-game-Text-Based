from .items import Items, CONSUMABLE, EQUIPPABLE
from .generate_items import _generate_items
from ..setup import DATA_ITEMS as DATA


def get_items(identify: str):
    identify = identify.split("@")
    
    count = 1
    name = identify[0]
    if len(identify) == 2:
        try: 
            count = int(identify[1])
        except ValueError:
            count = 1

    if name not in DATA["all_items"]:
        return

    classItems, name = name.split(":")
    return _generate_items(classItems, name=name, count=count)
