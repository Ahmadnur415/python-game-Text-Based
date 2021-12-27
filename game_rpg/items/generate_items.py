from ..setup import DATA_ITEMS, _ATTACK
from .items import Items, EQUIPPABLE, CONSUMABLE
from ..attack import Attack

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
    attack_in_items = items.get("attack", []).copy()
    attacks = []

    if not attack_in_items:
        return
    for attack in attack_in_items:
        if isinstance(attack, str):
            attack = _ATTACK[attack]

        if not attack.get("damage", None):
            attack["damage"] = items["damage"]

        attacks.append(Attack.load_attack(attack))

    return attacks
