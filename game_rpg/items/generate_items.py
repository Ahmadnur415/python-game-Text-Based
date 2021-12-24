from ..setup import DATA_ITEMS, _ATTACK
from .items import Items, EQUIPPABLE, CONSUMABLE
from ..attack import ATTACK

def generate_items( identify: str, count: int=1 ):
    if identify not in DATA_ITEMS["id"]:
        raise NameError
    
    names , items = identify.split("/")
    items = DATA_ITEMS["list"][names][items]

    if items["class"] == "EQUIPPABLE":
        return generate_items_EQUIPPABLE(items)
    if items["class"] == "CONSUMABLE":
        return generate_items_CONSUMABLE(items, count)


def generate_items_CONSUMABLE(items, count=1):
    if not items:
        return
    return Items(
        name=items["name"],
        quality=items["quality"],
        typeItems=items['type_items'],
        identify=items['identify'],
        attribute=CONSUMABLE(
            type_=items["attribute"]["type"],
            stats=items["attribute"]["stats"]
        ),
        price=items["price"],
        sub_stats=items.get("sub_stats", None),
        amount=count,
        in_shop=items.get("in_shop", True)
    )


def generate_items_EQUIPPABLE(items):
    if not items:
        return
    return Items(
        name=items["name"],
        quality=items["quality"],
        typeItems=items['type_items'],
        identify=items["identify"],
        attribute=EQUIPPABLE(
            location=items["location"],
            user=items["user"],
            styleAttack=items.get("styleAttack", None),
            attack=generate_attack_of_items(items),
            **{key: items.get(key, 0) for key in DATA_ITEMS["attribute"]["basic"]}
        ),
        price=items["price"],
        stats=items.get("stats", None),
        in_shop=items.get("in_shop", True)
    )


def generate_attack_of_items(items):
    list_of_attack = items.get("attack", []).copy()
    attacks = []

    if not list_of_attack:
        return

    for attack_in_items in list_of_attack:
        if isinstance(attack_in_items, str):
            attack_in_items = attack_in_items.split(":")
            if len(attack_in_items) == 2:
                try:
                    attack_in_items = _ATTACK[attack_in_items[0]][attack_in_items[1]]
                except KeyError:
                    continue

        # -----
        if not attack_in_items.get("base_damage", None):
            attack_in_items["base_damage"] = items["damage"]

        attacks.append(
            ATTACK(attack_in_items)
        )

    return attacks
