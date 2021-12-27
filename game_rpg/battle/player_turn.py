from .. import interface, namespace


def run_player_turn(battle):
    while True:
        battle.view_battle()
        interface.centerprint(
            "~",
            interface.get_messages("battle.actions.command").format(
                interface.generate_readable_list(namespace.BATTLE_TURN_COMMANDS, number=True)
            )
        )
        command = interface.get_input()
        print()
        
        if command in [str(i) for i in range(len(namespace.BATTLE_TURN_COMMANDS) + 1)]:
            command = namespace.BATTLE_TURN_COMMANDS[int(command) - 1]

        if command == namespace.USE_ITEMS:
            if battle.total_use_items == battle.max_use_items:
                interface.centerprint(interface.get_messages("limit_the_use_of_items"))
                interface.get_enter()
                continue
            
            result = battle.player.use_items_consumable_interface()
            
            if result:
                battle.total_use_items += 1

        if command == namespace.BATTLE_FLED:
            interface.centerprint(interface.get_messages("battle.actions.fled"), distance=0)
            result = interface.get_boolean_input()
            print()
            if result:
                battle.fled = True
                break
            continue

        if command == namespace.BATTLE_ATTACK:
            result = battle.player_attack_phase()
            # break
            if result != namespace.BACK:
                break
