import random
from ..entity import flag
from .. import interface


def run_enemy_turn(battle):

    if not battle.enemy.usable_attacks:
        pass

    player_health = battle.player.health
    attack_use = random.choice(battle.enemy.usable_attacks)

    result_attack = battle.enemy.attack_state(battle.player, attack_use)

    if result_attack == flag.EVADED:
        interface.centerprint(
            interface.get_messages("prefixes.player", "You") + " " + interface.get_messages("battle.messages.player_evaded")
        )
        return

    if result_attack == flag.CRITICAL_HIT:
        interface.print_(
            interface.get_messages("prefixes.enemy") + interface.get_messages("battle.messages.critical_hit")
        )

    damage = player_health - battle.player.health

    interface.centerprint(
        interface.get_messages(
            "battle.messages.damage_dealt"
        ).format(
            attack_description=attack_use.description_of_being_used,
            enemy=interface.get_messages("prefixes.player"),
            damage=str(damage),
            attacker=interface.get_messages("prefixes.enemy"),
            type_damage=attack_use.typeAttack
        )
    )
    return