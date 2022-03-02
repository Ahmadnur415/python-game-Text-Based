from copy import deepcopy
from .data import _load
from . import enemy, attack
import random


def create_enemy(name_enemy, level=1) -> enemy.Enemy:
    
    dt_enemy = _load("enemy.json")

    if name_enemy not in dt_enemy:
        raise NameError(f"{name_enemy} is not in data")

    dt = deepcopy(dt_enemy[name_enemy])

    for name, values in dt["stats"].items():
        for stat, value in values.items():

            if isinstance(value, list):
                value = random.randint(min(value), max(value))

            dt["stats"][name][stat] = value

    for location, values in dt["equipment"].items():

        if isinstance(values, list):
            values = random.choice(values)

        dt["equipment"][location] = values

    lootings = []
    if dt.get("looting"):
        for loot in sorted(dt["looting"], key=lambda d: d["change"], reverse=True):
            lootings.append((loot, loot["change"]))


    return enemy.Enemy(
        name=dt["name"],
        level=level,
        type_damage=dt["type_damage"],
        equipments=dt["equipment"],
        stats=dt["stats"],
        attacks=[ attack.load_from_id(_id) for _id in dt["attacks"].copy() ],
        looting=lootings,
        inventory=dt["inventory"].copy()
    )


def create_enemy_random(lv = 1, requirement_level=True):

    dt_enemy = _load("enemy.json")

    for _ in range(10):

        name_enemy = random.choice(list(dt_enemy.keys()))
        dt = dt_enemy[name_enemy]
        req_level = dt["requirement_level"]

        if not requirement_level or req_level == "-" or isinstance(req_level, int) and req_level <= lv:
            break

        if isinstance(req_level, list):
            if (req_level[0] < lv and isinstance(req_level[1], str) and req_level[1] == "-") or \
                (req_level[0] < lv and isinstance(req_level[1], int) and req_level[1] >= lv):
                break

    return create_enemy(name_enemy, lv)
