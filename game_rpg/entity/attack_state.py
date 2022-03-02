import random
import math
from ..battle import flag
from .. import util, namespace


def attack_state(self, enemy, attack_use):
    eveded_enemy = util.resolve_random_condition([
        (True, enemy.evaded),
        (False, 100 - enemy.evaded)
    ])

    if eveded_enemy:
        return flag.EVADED

    if not attack_use.user:
        attack_use.user = self

    damage = attack_use.damage.copy()

    # ===== GENERATE DAMAGE =====
    if isinstance(damage, list):
        
        for i, value in enumerate(damage.copy()):
            if isinstance(value, dict):
                damage[i] = util._generate_value_from_dict(damage[i], self, enemy)

        damage = random.randrange(damage[0], damage[1])

    if attack_use.modiefer_damage:
        damage += attack_use.get_modiefer_damage(enemy)

    damage *= (getattr(self, getattr(namespace.TYPE_ATTACK, attack_use.type_attack), 0) * 1.5 / 8)
    damage = math.floor(damage)

    enemy_defense_prior = enemy.defense
    enemy.defense -= int(enemy.defense * self.armor_penetration / 100)

    # ===== CRITICAL =====
    critical_change = util.resolve_random_condition([
        (True, util.clamp(self.critical_change, 0, 99)),
        (False, 100 - util.clamp(self.critical_change, 0, 99))
    ])


    # interface.print_("damage :", damage)
    if critical_change:
        damage += round(damage / 100 * self.critical_damage)
        # interface.print_("CRITICAL DAMAGE :", damage)

    # ===== DEAL DAMAGE =====
    reduce_damage = util.clamp( int(damage * enemy.reduce_damage.get( attack_use.type_damage, "physical" ) / 100), 1, 999999999 )

    # interface.print_("reduce damage percent : ", enemy.reduce_damage.get( attack_use.type_damage, "physical" ))
    # interface.print_("reduce damage final :", reduce_damage)
    damage -= reduce_damage

    # interface.print_("damage :", damage)

    enemy.health -= damage
    enemy.defense = enemy_defense_prior

    if critical_change:
        return flag.CRITICAL_HIT



