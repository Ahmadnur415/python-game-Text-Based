import random
from .. import until
from . import flag


def attack_state(attacker, enemy, attack_use):
    # ===== STAMINA AND MANA =====
    if attack_use.cost_st > attacker.stamina:
        return flag.NOT_ENOUGH_STAMINA

    if attack_use.cost_mp > attacker.mana:
        return flag.NOT_ENOUGH_MANA

    attacker.stamina -= attack_use.cost_st
    attacker.mana -= attack_use.cost_mp

    # ===== EVASION =====
    evaded_enemy = until.resolve_random_condition([
        (True, enemy.evaded),
        (False, 100 - enemy.evaded)
    ])

    if evaded_enemy:
        return flag.EVADED

    # ===== ARMOR =====
    enemy_defense = enemy.defense
    enemy.defense -= int(enemy.defense * attacker.armor_penetration / 100)

    damage = attacker._generate_damage_of_attack_use(enemy, attack_use)
    damage = random.randint(min(damage), max(damage))

    # ===== CRITICAL =====
    critical_change = until.resolve_random_condition([
        (True, until.clamp(attacker.critical_change, 0, 99)),
        (False, 100 - until.clamp(attacker.critical_change, 0, 99))
    ])

    if critical_change:
        damage += round(damage / 100 * attacker.critical_hit)

    # ===== DEAL DAMAGE =====
    damage -= until.clamp(
        int(damage * enemy.reduce_damage.get(attack_use.typeAttack, "physical") / 100),
        1,
        damage - 1
    )
    enemy.health -= until.clamp(damage, 1, 99999)
    enemy.defense = enemy_defense

    if critical_change:
        return flag.CRITICAL_HIT


def _generate_damage_of_attack_use(attacker, enemy, attack_use):
    damage = [1, attack_use.base_damage] if isinstance(attack_use.base_damage, (int, float)) else attack_use.base_damage
    for multiplier in attack_use.multiplier:
        if isinstance(multiplier.stats, (int, float)):
            damage = [a + int(multiplier.stats * multiplier.modifier) for a in damage]
            continue

        values = 0
        if isinstance(multiplier.stats, str):
            entity = multiplier.stats.split(".")[0].lower()
            stats = multiplier.stats.split(".")[-1]
            values = getattr(
                attacker if entity == "self" else enemy,
                stats,
                0
            )
        if isinstance(values, dict):
            values = values[attack_use.typeAttack]

        if isinstance(values, list):
            damage = [a + int(b * multiplier.modifier) for a, b in zip(damage, values)]
            continue

        if isinstance(values, (int, float)):
            damage = [a + int(values * multiplier.modifier) for a in damage]
            continue

    return sorted(damage)


@property
def usable_attacks(entity):
    usable_attacks_list = []

    for attack in entity.attack:
        if (
            entity.mana >= attack.cost_mp and entity.stamina >= attack.cost_st
        ):
            usable_attacks_list.append(attack)

    return usable_attacks_list