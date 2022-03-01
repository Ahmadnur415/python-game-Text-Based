from .data import _load
from . import enemy, attack
import random


dt_enemy = _load("enemy.json")


def create_enemy(name_enemy, level=1) -> enemy.Enemy:

    if name_enemy not in dt_enemy:
        raise NameError("Nama Enemy salah, " + str(name_enemy))

    data = dt_enemy[name_enemy]

    stats = data["stats"].copy()

    for name, values in stats.items():
        for stat, value in values.items():

            if isinstance(value, list):
                value = random.randint(min(value), max(value))

            stats[name][stat] = value


    equipments = data["equipment"].copy()

    for location, values in equipments.items():

        if isinstance(values, list):
            values = random.choice(values)

        equipments[location] = values

    # looting
    lootings = []
    if data.get("looting"):
        looting_sorted = sorted(data["looting"].copy(), key=lambda d: d["change"], reverse=True)
        for loot in looting_sorted:
            lootings.append((loot, loot["change"]))


    return enemy.Enemy(
        name=data["name"],
        level=level,
        type_damage=data["type_damage"],
        equipments=equipments,
        stats=stats,
        attacks=[ attack.load_from_id(_id) for _id in data["attacks"].copy() ],
        looting=lootings,
        inventory=data["inventory"].copy()
    )


def create_enemy_random(lv = 1, requirement_level=True):

    name_enemy = random.choice(list(dt_enemy.keys()))
    r_enemy = dt_enemy[name_enemy]
    req_level = r_enemy["requirement_level"]

    i = 0
    while requirement_level and i != 10:

        if req_level == "-":
            break

        if isinstance(req_level, int) and req_level <= lv:
            break

        if isinstance(req_level, list):
            if (req_level[0] < lv and isinstance(req_level[1], str) and req_level[1] == "-") or \
                (req_level[0] < lv and isinstance(req_level[1], int) and req_level[1] >= lv):
                break

        name_enemy = random.choice(list(dt_enemy.keys()))
        r_enemy = dt_enemy[name_enemy]
        req_level = r_enemy["requirement_level"]

        i += 1

    return create_enemy(name_enemy, lv)
