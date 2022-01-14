from .. import interface, namespace
from ..entity import flag


def player_attack_phase(battle):
    display_name = interface.get_messages("prefixes.player", "You") + " "
    while True:
        print()
        battle.print_list_of_attacks()        
        index = "1" if len(battle.player.attack) == 1 else (f"1 - {len(battle.player.attack)}")

        # print: choise attack player 
        interface.centerprint("== " + interface.get_messages("input_messages.choose_items_interface").format(name="Attack",index=index) + " ==")
        attack_name = interface.get_input()
        
        if attack_name.lower() == "b":
            return namespace.BACK

        try:
            attack_name = battle.player.attack_name[int(attack_name) - 1]
        except (ValueError, IndexError):
            continue
    
        if attack_name not in battle.player.attack_name:
            continue
        
        # get attack
        attack_use = battle.player.get_attack_from_name(attack_name)

        if attack_use.cooldown < attack_use.countdown:
            continue
        
        # ===== STAMINA AND MANA =====
        if attack_use.cost_st > battle.player.stamina:
            interface.centerprint(display_name + interface.get_messages("battle.messages.not_enough_stamina"))
            interface.get_enter()
            continue

        if attack_use.cost_mp > battle.player.mana:
            interface.centerprint(display_name + interface.get_messages("player.display_name", "you") + interface.get_messages("battle.messages.not_enough_mana"))
            interface.get_enter()
            continue

        battle.player.stamina -= attack_use.cost_st
        battle.player.mana -= attack_use.cost_mp

        return battle.player_attack(attack_use)

def player_attack(battle, attack_use):
    display_name = interface.get_messages("prefixes.player", "You")
    count_raw_attack = attack_use.raw_attack
    print("\n")
    while count_raw_attack > 0:
        proir_health = battle.enemy.health
        attack_result = battle.player.attack_state(battle.enemy, attack_use)

        if attack_result == flag.EVADED:
            battle.count_dodge += 1
            interface.centerprint(interface.get_messages("prefixes.enemy") + interface.get_messages("battle.messages.enemy_evaded"))
            count_raw_attack -= 1
            continue

        if attack_result == flag.CRITICAL_HIT:
            battle.count_crit += 1
            interface.centerprint( display_name + interface.get_messages("battle.messages.critical_hit") )

        deal_damage = proir_health - battle.enemy.health
        count_raw_attack -= 1

        interface.leftprint(
            interface.get_messages("battle.messages.damage_dealt").format(
                attack_description=attack_use.description_of_being_used,
                enemy=interface.get_messages("prefixes.enemy"),
                damage=str(deal_damage),
                attacker=interface.get_messages("prefixes.player") + "'s",
                type_damage=attack_use.type_damage
            )
        )

    print()
    attack_use.cooldown = 0