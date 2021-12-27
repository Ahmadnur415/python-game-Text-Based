# Generate Enemy

from .enemy import Enemy
from .setup import _ATTACK, GAME
from .file import _load
from .items import get_items, Items as ITEMS, EQUIPPABLE
from .attack import Attack
import random
import _collections_abc

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
    _ENEMY = _load(GAME["fileGame"]["enemy"])
    if isinstance(lv, (list, tuple)):
        lv = random.randint(min(lv), max(lv))

    _class = random.choice(_ENEMY["list_enemy"].copy())
    DATA = _ENEMY["class"][_class].copy()
    if _class in _ENEMY["variant"]:
        variant_enemy = random.choice(_ENEMY["variant"][_class].copy() + ["default"])
        if variant_enemy != "default":
            DATA = update_enemy(DATA, variant_enemy)

    # -- equipment
    equipment = {}
    if DATA.get("equipment"):
        for locate, values  in DATA["equipment"].items():
            id_items = random.choice(values) if isinstance(values, list) else values
            items = get_items(id_items)
            if not isinstance(items, ITEMS) or not isinstance(items.attribute, EQUIPPABLE):
                # gagal dalam mendapatka items
                continue

            if locate == "hand":
                locate = random.choice(items.attribute.location)

            equipment[locate] = items

    # for attack enemy
    attacks = []
    if DATA.get("attack"):
        for attack in DATA["attack"].copy():

            if isinstance(attack, str):
                attack = _ATTACK[attack]
            
            if isinstance(attack, dict):
                attacks.append(Attack.load_attack(attack))
                continue
    
    # looting
    looting = []
    if DATA.get("looting"):
        looting_sorted = sorted(DATA["looting"], key=lambda d: d["change"], reverse=True)
        for loot in looting_sorted:
            looting.append((loot, loot["change"]))

    return Enemy(
        name=DATA["name"],
        _class=_class,
        level=lv,
        attacks=attacks,
        equipments=equipment,
        stats=DATA,
        looting=looting
    )

def update_enemy(orig_data: dict, new_data: dict):
    for key, value in new_data.items():
        if isinstance(value, _collections_abc.Mapping):
            orig_data[key] = update_enemy(orig_data.get(key, {}), value)
        else:
            orig_data[key] = value
    return orig_data