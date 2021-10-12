from ..setup import DATA_ITEMS, _ATTACK
from .items import Items, EQUIPPABLE, CONSUMABLE
from ..attack import ATTACK, AttackStyle


def _generate_items(classItems, index=1, name=None, count=1) -> Items:
    if classItems not in DATA_ITEMS["items"]:
        return

    DATA = DATA_ITEMS["items"][classItems].copy()

    if index > len(list(DATA["items"].keys())) or index <= 0:
        return

    if name not in DATA["items"]:
        name = list(DATA["items"].keys())[int(index) - 1]

    items = DATA["items"][name].copy()

    if DATA["class"] == "EQUIPPABLE":
        return Items(
            name=items["name"],
            quality=items["quality"],
            typeItems=items['type_items'],
            identify=items["identify"],
            attribute=EQUIPPABLE(
                location=items["location"],
                user=items["user"],
                styleAttack=AttackStyle.get(items.get("styleAttack", None), None),
                attack=_generate_attack_of_items(items),
                classItems=items["classItems"],
                **{key: items.get(key, 0) for key in DATA_ITEMS["attribute"]["basic"]}
            ),
            price=items["price"],
            sub_stats=items.get("sub_stats", {}),
            in_shop=items.get("in_shop", True)
        )

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
        sub_stats=items.get("sub_stats", {}),
        amount=count
    )


def _generate_items_CONSUMABLE(items, count=1):
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
        amount=count
    )


def _generate_items_EQUIPPABLE(items):
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
            styleAttack=items["styleAttack"],
            attack=items["attack"],
            classItems=items["classItems"],
            **{key: items.get(key, 0) for key in DATA_ITEMS["attribute"]["basic"]}
        ),
        price=items["price"],
        sub_stats=items.get("sub_stats", None)
    )


def _generate_attack_of_items(items):
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
