# Generate Enemy

from .enemy import Enemy
from .setup import _ENEMY, _ATTACK
from .items import get_items, Items as ITEMS, EQUIPPABLE
from .attack import ATTACK
import random


def _generate_enemy_level(lv: int, diff: int=1):
    if 3 < lv <= 7:
        lv = (1, lv)
    elif lv > 7:
        if lv < 58:
            max_lv = lv + diff
            if max_lv > 60:
                max_lv = 60
            lv = (lv - int(4  - (1.5 * diff)) , max_lv)
        elif lv >= 58:
            lv = (57 - int(4  - (1.5 * diff)), lv)

    return lv


def enemyRandom(lv=3):
    if isinstance(lv, (list, tuple)):
        lv = random.randint(min(lv), max(lv))

    _class = random.choice(_ENEMY["class_enemy"].copy())
    DATA = _ENEMY["class"][_class].copy()
    if _class in _ENEMY["variant"]:
        variant_enemy = random.choice(_ENEMY["variant"][_class].copy() + ["default"])
        if variant_enemy != "default":
            DATA["stats"].update(variant_enemy.get("stats", {}))
            variant_enemy.pop("stats", None)
            DATA.update(variant_enemy)

    # -- equipment
    equipment = {}
    if DATA.get("equipment"):
        for locate, values  in DATA["equipment"].items():
            id_items = random.choice(values) if isinstance(values, list) else values
            items = get_items(id_items)
            if not isinstance(items, ITEMS):
                # gagal dalam mendapatka items
                continue
            
            if not isinstance(items.attribute, EQUIPPABLE):
                continue
            

            if locate == "hand":
                locate = random.choice(items.attribute.location)

            equipment[locate] = items

    # for attack enemy
    attacks = []
    if DATA.get("attack"):
        for attack in DATA["attack"].copy():

            if isinstance(attack, str):
                attack = attack.split(":")
                attack = _ATTACK[attack[0]][attack[1]]
            
            if isinstance(attack, dict):
                attacks.append(ATTACK(attack))
                continue
    
    # looting
    looting = []
    if DATA.get("looting"):
        print("aaaa")
        for loot, change in DATA["looting"].items():
            looting.append((loot, change))


    return Enemy(
        name=DATA["name"],
        _class=_class,
        level=lv,
        attacks=attacks,
        equipments=equipment,
        stats=DATA,
        looting=looting
    )