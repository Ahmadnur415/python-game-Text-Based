from .. import interface, namespace
from . import flag

def player_attack_phase(battle):
    while True:
        battle.print_list_of_attacks_player()
        command = interface.get_command(battle.player.attacks, loop=False)

        if not isinstance(command, tuple):
            continue

        interface.print_("\n")
        if command[0] == namespace.BACK:
            return command[0]

        attack_use = battle.player.attacks[command[1] - 1]

        if attack_use.cooldown > 0:
            battle.print_message("on_cooldown", attack_use.name, attack_use.cooldown)
            interface.get_enter()
            continue

        if attack_use.cost_stamina > battle.player.stamina:
            battle.print_message("not_enough_stamina", battle.get_prefixes(battle.player))

            interface.get_enter()
            continue

        if attack_use.cost_mana > battle.player.mana:
            battle.print_message("not_enough_mana", battle.get_prefixes(battle.player))
            interface.get_enter()
            pass

        battle.player.stamina -= attack_use.cost_stamina
        battle.player.mana -= attack_use.cost_mana

        proir_health = battle.enemy.health
        # attack ----
        result_battle = battle.player.attack_state(battle.enemy, attack_use)
        attack_use.cooldown = attack_use.countdown

        interface.centerprint("-", width=battle.width_line)
        if result_battle == flag.EVADED:
            battle.print_message( "enemy_evaded", battle.get_prefixes(battle.enemy) )
            return

        if result_battle == flag.CRITICAL_HIT:
            battle.count_crit_player += 1
            battle.print_message( "critical_hit", battle.get_prefixes(battle.player) )

        damage = proir_health - battle.enemy.health

        battle.print_deal_damage(
            battle.enemy,
            attack_use,
            damage
        )
        return