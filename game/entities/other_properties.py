import functools
from typing import TYPE_CHECKING, Dict

from ..utils import clamp

if TYPE_CHECKING:
    from .entity_stats import EntityStats


def _global_var(stats: "EntityStats"):
    global STR, DEX, MGC, PERC, CON, WILL, G_HP, G_MP, B_CRIT_CHG, B_CRIT_DMG, B_HP, B_MP, B_ST, B_MAX_HP, B_MAX_MP, B_MAX_ST, LV, EVE, DEF, RES

    STR = stats.strength
    DEX = stats.dexterity
    MGC = stats.magic
    PERC = stats.perception
    CON = stats.constitution
    WILL = stats.will
    G_HP = stats.growth_hp
    G_MP = stats.growth_mp
    B_CRIT_CHG = stats.base_critical_change
    B_CRIT_DMG = stats.base_critical_damage
    B_HP = stats.base_health
    B_MP = stats.base_mana
    B_ST = stats.base_stamina
    B_MAX_HP = stats.base_max_health
    B_MAX_MP = stats.base_max_mana
    B_MAX_ST = stats.base_max_stamina

    EVE = stats.base_evasion
    DEF = stats.base_defense
    RES = stats.base_resistance

    LV = getattr(stats, "level", 0)


def init(func):
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        _global_var(self)
        return func(self, *args, **kwargs)

    return wrapper


@property
@init
def max_health(self: "EntityStats") -> int:
    MULTIPLIER = G_HP / 100
    BONUS = 5 * LV
    HP = (13 * CON + 4 * WILL + STR) / 3 + BONUS
    HP *= MULTIPLIER
    return int(B_MAX_HP + HP)


@property
@init
def max_mana(self: "EntityStats") -> int:
    """
    1 WILL  : 3.3
    1 MGC   : 0.6
    1 LV    : 3
    """
    MULTIPLIER = G_MP / 100
    BONUS = 3 * LV
    MP = (10 * WILL + 2 * MGC) / 3 + BONUS
    MP *= MULTIPLIER
    return int(B_MAX_MP + MP)


@property
@init
def max_stamina(self: "EntityStats") -> int:
    """
    1 DEX     : 0.5
    1 PERC    : 0.7
    1 STR     : 0.3
    1 CON     : 0.5
    1 LV      : 4
    """
    BONUS = 4 * LV
    ST = (2.1 * PERC + 1.5 * DEX + 0.9 * STR + 1.5 * CON) / 3 + BONUS
    return round(B_MAX_ST + ST)


@property
@init
def critical_change(self: "EntityStats") -> float:
    """
    1 PERC      : 0.05
    1 DEX       : 0.03
    1 STR       : 0.03
    1 MGC       : 0.03
    1 LV        : 0.01
    """
    BONUS = LV / 100
    CRIT = 0.05 * PERC + ((DEX + STR + MGC) / 3) / 30 + BONUS
    RESULT = round(CRIT + B_CRIT_CHG, 2)
    return clamp(RESULT, 0, 100)


@property
@init
def critical_damage(self: "EntityStats") -> float:
    """
    1 STR   : 0.4
    1 DEX   : 0.2
    1 MGC   : 0.4
    """
    DMG = (2 * STR + DEX + 2 * MGC) / 5
    RESULT = 100 - 10000 / (100 + DMG)
    RESULT = round(B_CRIT_DMG + RESULT, 2)
    return RESULT


@property
@init
def evaded(self: "EntityStats") -> float:
    """
    1 EVE   : 0.15
    1 PERC  : 0.05
    1 WILL  : 0.05
    """
    RESULT = (3 * EVE + PERC + WILL) / 20
    RESULT = 100 - 10000 / (100 + RESULT)
    return round(RESULT, 2)


@property
def reduce_damage(self: "EntityStats") -> Dict[str, float]:
    return {"magic": self.magic_attack_reduce, "physical": self.physical_attack_reduce}


@property
@init
def physical_attack_reduce(self: "EntityStats") -> float:
    """
    1 DEF = 0.1
    1 CON = 0.01
    1 WILL = 0.01
    """
    RESULT = (10 * DEF + CON + WILL) / 100
    RESULT = 100 - 10000 / (100 + RESULT)
    return round(RESULT, 2)


@property
@init
def magic_attack_reduce(self: "EntityStats") -> float:
    """
    1 RES = 0.1
    1 MGC = 0.01
    1 WILL = 0.01
    """
    RESULT = (10 * RES + MGC + WILL) / 100
    RESULT = 100 - 10000 / (100 + RESULT)
    return round(RESULT, 2)
