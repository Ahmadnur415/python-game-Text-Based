import random
from ..entity import flag
from .. import interface


def run_enemy_turn(battle):

    if not battle.enemy.usable_attacks:
        return

    attack_use = random.choice(battle.enemy.usable_attacks)

    count_raw_attack = attack_use.raw_attack
    while count_raw_attack > 0:

        player_health = battle.player.health
        result_attack = battle.enemy.attack_state(battle.player, attack_use)

        if result_attack == flag.EVADED:
            interface.centerprint( interface.get_messages("prefixes.player", "You") + " " + interface.get_messages("battle.messages.player_evaded") )
            continue

        if result_attack == flag.CRITICAL_HIT:
            interface.centerprint( interface.get_messages("prefixes.enemy") + interface.get_messages("battle.messages.critical_hit") )

        damage = player_health - battle.player.health

        interface.leftprint(
            interface.get_messages(
                "battle.messages.damage_dealt"
            ).format(
                attack_description=attack_use.description_of_being_used,
                enemy=interface.get_messages("prefixes.player"),
                damage=str(damage),
                attacker=interface.get_messages("prefixes.enemy"),
                type_damage=attack_use.type_damage
            )
        )
        count_raw_attack -= 1
    attack_use.cooldown = 0
    return