from .items import Items, EQUIPPABLE, CONSUMABLE
from .generate_items import generate_items


def get_items(identify: str, amount=1):
    try:
        return generate_items(identify, amount)
    except NameError:
        print(f"Cannot Load items : identify Error \"{identify}\"")
        return 