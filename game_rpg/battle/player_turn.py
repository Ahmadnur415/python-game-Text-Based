from .. import interface
from ..entity import flag


def run_player_turn(battle):
    while True:
        # view battle
        battle.view_battle()
        interface.centerprint(
            "~",
            interface.get_messages("battle.actions.command").format(
                interface.generate_readable_list(battle.TURN_COMMANDS, number=True)
            )
        )
        command = interface.get_input()
        print()

        if command in [str(i) for i in range(1, len(battle.TURN_COMMANDS) + 1)]:
            command = battle.TURN_COMMANDS[int(command) - 1]

        if command == battle.USE_ITEMS:
            result = battle.player.use_items_consumable_interface()
            if result != battle.BACK:
                break

        if command == battle.FLED:
            interface.centerprint(interface.get_messages("battle.actions.fled"), distance=0)
            result = interface.get_boolean_input()
            print()
            if result:
                battle.fled = True
                break
            continue

        if command == battle.ATTACK:
            result = battle.player_attack_phase()
            # break
            if result != battle.BACK:
                break

def player_attack_phase(battle):
    while True:
        print()
        battle.print_list_of_attacks()        
        index = "1" if len(battle.player.attack) == 1 else f"1 - {len(battle.player.attack)}"

        # choise attack player 
        interface.centerprint("== " +interface.get_messages("input_messages.choose_items_interface").format(name="Attack",index=index) + " ==")
        attack_name = interface.get_input()
        
        if attack_name.lower() == "b":
            return battle.BACK

        try:
            attack_name = battle.player.attack_name[int(attack_name) - 1]
        except (ValueError, IndexError):
            continue
    
        if attack_name not in battle.player.attack_name:
            continue
        
        attack = battle.player.get_attack_from_name(attack_name)
        proir_health = battle.enemy.health
        attack_result = battle.player.attack_state(battle.enemy, attack)

        print()
        display_name_player = interface.get_messages("prefixes.player", "You") + " "

        if attack_result == flag.NOT_ENOUGH_MANA:
            interface.centerprint(display_name_player + interface.get_messages("player.display_name", "you") + " " + interface.get_messages("battle.messages.not_enough_mana"))
            interface.get_enter()
            continue

        if attack_result == flag.NOT_ENOUGH_STAMINA:
            interface.centerprint(display_name_player + interface.get_messages("battle.messages.not_enough_stamina"))
            interface.get_enter()
            continue

        if attack_result == flag.EVADED:
            battle.count_dodge += 1
            interface.centerprint(interface.get_messages("prefixes.enemy") + interface.get_messages("battle.messages.enemy_evaded"))
            break

        if attack_result == flag.CRITICAL_HIT:
            battle.count_crit += 1
            interface.print_(
                display_name_player + interface.get_messages("battle.messages.critical_hit")
            )

        deal_damage = proir_health - battle.enemy.health

        # print deal damage
        interface.centerprint(
            interface.get_messages("battle.messages.damage_dealt").format(
                attack_description=attack.description_of_being_used,
                enemy=interface.get_messages("prefixes.enemy"),
                damage=str(deal_damage),
                attacker=interface.get_messages("prefixes.player") + "'s",
                type_damage=attack.typeAttack
            )
        )
        # stop
        break
