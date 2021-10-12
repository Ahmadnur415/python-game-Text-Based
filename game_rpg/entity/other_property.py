from ..items import Items as ITEMS
from ..setup import DATA_ENTITY
from ..until import clamp
# import math


def _init(entity):
    global CON, STR, ARC, PERC, MGC, WILL, LUCK, WILL, LUCK, LV, GROWTH_HP, GROWTH_MP, DEF, EVE, RES
    CON = getattr(entity, "constitution", 0)
    STR = getattr(entity, "strength", 0)

    ARC = getattr(entity, "archery", 0)
    PERC = getattr(entity, "perception", 0)

    MGC = getattr(entity, "magic", 0)
    WILL = getattr(entity, "will", 0)

    LUCK = getattr(entity, "luck", 0)
    LV = getattr(entity, "level", 1)

    GROWTH_HP = getattr(entity, "growth_hp", 0)
    GROWTH_MP = getattr(entity, "growth_mp", 0)

    DEF = getattr(entity, "defense", 0)
    EVE = getattr(entity, "evasion", 0)
    RES = getattr(entity, "resistance", 0)


# ===========
# Reduce
# ===========
def physical_reduce(entity):
    # 1 point = 8 def | 12 CON
    _init(entity)
    bonus = 0
    for items in entity.equipment.values():
        if items:
            bonus += items.attribute.defense

    total = ((DEF + bonus + CON / 2) / 8) * (LUCK / 100)
    return clamp(100 - 10000 / (100 + total), 1, 95)


def magic_reduce(entity):
    # 1 magic reduce = 8 RES | 12 WILL
    _init(entity)
    bonus = 0
    for items in entity.equipment.values():
        if items:
            bonus += items.attribute.resistance

    total = ((RES + bonus + WILL / 2) / 8) * (LUCK / 100)
    return clamp(100 - 10000 / (100 + total), 1, 95)


# NOTE ==================== WIP ====================
@property
def evaded(entity):
    # 1 evaded = 8 EVE / 20 PERC / 16 WILL
    _init(entity)

    bonus = 0
    for items in entity.equipment.values():
        if items:
            bonus += items.attribute.evasion
    total = ((EVE + bonus + PERC / 2.5 + WILL / 2) / 8) * LUCK / 100
    return clamp(round(100 - 10000 / (100 + total), 2), 0, 95)


@property
def reduce_damage(entity):
    return {"physical": physical_reduce(entity), "magic": magic_reduce(entity)}


# =========
# resaurce
# =========

@property
def max_health(entity):
    # 3 HP / 1 CON :- 1 HP / 10 STR :- 1 HP / 5 WILL
    _init(entity)
    HP = GROWTH_HP * ((CON * 70 + WILL * 5 + STR * 2) / 21 + (clamp(40 - 0.22 * LV, 0, 99999) * LV)) / 100
    return int(HP + getattr(entity, "_max_health", 0))


@property
def max_mana(entity):
    # 3 MP / 1 WIlL :- 1 MP / 5 MGC
    _init(entity)
    MP = GROWTH_MP * ((25 * WILL + MGC * 2) / 10 + 5 * LV / 2) / 100
    return int(MP + getattr(entity, "_max_mana", 0))


@property
def max_stamina(entity):
    # 1 ST / 4 ARC :- 1 ST / 2 PERC :- 1 ST / 2 STR
    _init(entity)
    ST = (3 * ARC + 10 * PERC + 6 * STR + 25 * LV) / 12
    return int(ST  + getattr(entity, "_max_stamina", 0))


@property
def critical_change(entity):
    # 1 Crit / 4 PERC / 15 STR / 30 ARC / 30 MGC / 3 LV

    _init(entity)

    bonus = 0
    # equipment bonus
    for items in entity.equipment.values():
        if isinstance(items, ITEMS):
            bonus += items.sub_stats.get("critical_change", 0)

    crit = (PERC / 4) + (STR * 2 + ARC + MGC) / 30 + (0.3 * LV) + clamp(LUCK / 100, 1.0, 25.0)
    return clamp(round(crit + bonus, 2), 1, 99)


@property
def critical_hit(entity):
    _init(entity)

    bonus = 0
    # equipment bonus
    for items in entity.equipment.values():
        if isinstance(items, ITEMS):
            bonus += items.sub_stats.get("critical_hit", 0)

    dmg = (4 * STR + 4 * ARC + 4 * MGC + 3 * PERC + 2 * CON) / 7  + (LV * LUCK / 300)
    return round(dmg + 20 + bonus, 2)


# ==========
# damage
# ==========

@property
def damage(entity):
    _init(entity)
    floor = int

    physical = [
        max(LV + floor(STR / 3 + ARC / 5), 1), 
        max(floor(1.5 + 1.2 * LV) + floor(STR / 3 + ARC / 2), 1)
    ]
    magic = [
        max(LV + floor(MGC / 4 + (MGC + WILL) / 15), 1),
        max(floor(1.5 + 1.2 * LV) + floor(MGC / 2 + (MGC + WILL) / 15), 1)
    ]

    for locate, equipment in entity.equipment.items():
        if not equipment or locate not in DATA_ENTITY["attribute"]["equipment"]["weapons"]:
            continue

        multiplier = 1.1 if equipment.attribute.styleAttack.damage_stats == entity.style_attack else 0.75

        # menambahkan damage 
        if equipment.attribute.styleAttack.damage_stats == "magic":
            magic = [a + floor(b * multiplier) for a, b in zip(magic, equipment.attribute.damage)]
        else:
            physical = [a + floor(b * multiplier) for a, b in zip(physical, equipment.attribute.damage)]
    
    return {
        "physical": physical,
        "magic": magic
    }


@property
def magic_damage(entity):
    return entity.damage["magic"]


@property
def physical_damage(entity):
    return entity.damage["physical"]


@property
def max_exp(entity):
    _init(entity)
    return int((175 * LV + 50) / 3.14)
