from ..util import clamp


def _init(entity):
    global CON, STR, DEX, PERC, MGC, WILL, LV, GROWTH_HP, GROWTH_MP, DEF, EVE, RES

    CON = getattr(entity, "constitution", 0)
    STR = getattr(entity, "strength", 0)
    DEX = getattr(entity, "dextery", 0)
    PERC = getattr(entity, "perception", 0)
    MGC = getattr(entity, "magic", 0)
    WILL = getattr(entity, "will", 0)
    LV = getattr(entity, "level", 1)
    GROWTH_HP = getattr(entity, "growth_hp", 0)
    GROWTH_MP = getattr(entity, "growth_mp", 0)
    DEF = getattr(entity, "defense", 0)
    EVE = getattr(entity, "evasion", 0)
    RES = getattr(entity, "resistance", 0)


def physical_attack_reduce(entity):
    _init(entity)

    _reduce = sum(
        [item.stats["basic"].get("defense", 0) for item in entity.equipment.values() if item]
    )

    T_R = ((DEF * 1.5  + _reduce + CON / 2) / 8)
    return clamp(100 - 10000 / (100 + T_R), 1, 95)


def magic_attack_reduce(entity):
    _init(entity)

    _reduce = sum(
        [item.stats["basic"].get("resistance", 0) for item in entity.equipment.values() if item]
    )

    T_R = ((RES * 1.5  + _reduce + WILL / 2)/ 8)
    return clamp(100 - 10000 / (100 + T_R), 1, 95)


@property
def attack_reduce(entity):
    return {
        "physical": entity.physical_attack_reduce(),
        "magic": entity.magic_attack_reduce()
    }


@property
def evaded(entity):
    _init(entity)

    B_EVE = sum(
        [item.stats["basic"].get("evasion", 0) for item in entity.equipment.values() if item]
    )

    T = ((EVE * 1.5 + B_EVE + PERC / 2.5 + WILL / 2) / 8)
    return clamp(round(100 - 10000 / (100 + T), 2), 0, 95)


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
    # 1 ST / 4 DEX :- 1 ST / 2 PERC :- 1 ST / 2 STR
    _init(entity)
    ST = (3 * DEX + 10 * PERC + 6 * STR + 25 * LV) / 12
    return int(ST  + getattr(entity, "_max_stamina", 0))


@property
def critical_change(entity):
    _init(entity)
    crit = (PERC / 10) + (STR + DEX + MGC) / 30 + clamp(0.17 * LV, 1, 25)
    return clamp(round(crit + getattr(entity, "_critical_change", 0), 2), 1, 99)


@property
def critical_damage(entity):
    _init(entity)
    dmg = (4 * STR + 4 * DEX + 4 * MGC + 3 * PERC + 2 * CON) / 7
    return round(dmg + 20 + getattr(entity, "_critical_damage", 0), 2)


@property
def attacks(self) -> list:
    from ..attack import load_from_id
    _attacks = self._attacks.copy()
    for item in self.equipment.values():
        if item:
            for attack in item.attacks:
                attack.user = self
                _attacks.append(attack)
    
    punch = load_from_id("melee/punch")
    punch.user = self

    _attacks.append(punch)
    return _attacks


@property
def usable_attacks(self):
    usable_attacks_list = []
    for attack in self.attacks:
        if (
            self.mana >= attack.cost_mana and self.stamina >= attack.cost_stamina and attack.cooldown <= 0
        ):
            usable_attacks_list.append(attack)
    return usable_attacks_list


@property
def max_exp(entity):
    _init(entity)
    return int((175 * LV + 50) / 3.14)
