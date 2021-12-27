import random
from .. import until
from . import flag


def attack_state(attacker, enemy, attack_use):
    # ===== EVASION =====
    evaded_enemy = until.resolve_random_condition([
        (True, enemy.evaded),
        (False, 100 - enemy.evaded)
    ])

    if evaded_enemy:
        return flag.EVADED

    # ===== DAMAGE ====-
    persentance_damage = (100 + (10 * attack_use.raw_attack - 10)) / attack_use.raw_attack
    damage = attack_use.generate_damage(attacker, enemy)
    if min(damage) != max(damage):
        damage = random.randrange(min(damage), max(damage))
    else:
        damage = damage[0]
    damage = round(damage * persentance_damage / 100)

    # ===== ARMOR =====
    enemy_defense = enemy.defense
    enemy.defense -= int(enemy.defense * attacker.armor_penetration / 100)

    # ===== CRITICAL =====
    critical_change = until.resolve_random_condition([
        (True, until.clamp(attacker.critical_change, 0, 99)),
        (False, 100 - until.clamp(attacker.critical_change, 0, 99))
    ])

    if critical_change:
        damage += round(damage / 100 * attacker.critical_hit)

    # ===== DEAL DAMAGE =====
    damage -= until.clamp(
        int(damage * enemy.reduce_damage.get(attack_use.type_damage, "physical") / 100), 1, damage - 1 )

    enemy.health -= damage
    enemy.defense = enemy_defense

    if critical_change:
        return flag.CRITICAL_HIT


@property
def usable_attacks(entity):
    usable_attacks_list = []

    for attack in entity.attack:
        if (
            entity.mana >= attack.cost_mp and entity.stamina >= attack.cost_st and attack.cooldown >= attack.countdown
        ):
            usable_attacks_list.append(attack)

    return usable_attacks_list


def attack_turn_count(entity):
    for attack in entity.attack:
        attack.cooldown += 1