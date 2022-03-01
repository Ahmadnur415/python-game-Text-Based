import random
from . import flag
from .. import interface

def enemy_attack_phase(battle):

    if not battle.enemy.usable_attacks:
        return

    attack_use = random.choice(battle.enemy.usable_attacks)
    proir_health = battle.player.health

    result_attack = battle.enemy.attack_state(battle.player, attack_use)

    if result_attack == flag.EVADED:
        battle.count_dodge_player += 1
        battle.print_mesagge("player_evaded")
        interface.get_enter()
        return

    if result_attack == flag.CRITICAL_HIT:
        battle.print_message("critical_hit", battle.get_prefixes(battle.enemy))

    attack_use.cooldown = attack_use.countdown
    damage = proir_health - battle.player.health
    battle.print_deal_damage(
        battle.player,
        attack_use,
        damage
    )
    interface.centerprint("-")
