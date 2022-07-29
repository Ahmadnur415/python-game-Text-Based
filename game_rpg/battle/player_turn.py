from .. import interface, namespace


def player_turn(battle):

    while battle.player:

        USE_ITEMS = interface.get_messages("battle.actions.use_item").format(battle.max_use_items - battle.count_use_items)
        commands = [namespace.BATTLE_ATTACK, USE_ITEMS, namespace.BATTLE_FLED]

        battle.view()

        interface.leftprint(
            interface.get_messages("battle.actions.command"),
            *interface.generate_readable_list(commands, number=True, make_line=False),
            width=battle.width_line
        )

        command = interface.get_command(commands, "Action", add_command_back=False, loop=False)

        if not isinstance(command, tuple):
            continue

        interface.print_("\n")
        if command[0] == USE_ITEMS:

            if battle.count_use_items > battle.max_use_items:
                battle.print_message("limit_the_use_of_items")

                continue

            result = battle.player.consumable_interface()

            if not result:
                interface.get_enter()

            if result and result != namespace.BACK:
                battle.count_use_items += 1
            interface.print_("\n")

            continue

        if command[0] == namespace.BATTLE_FLED:
            battle.print_message("fled")
            battle.fled = interface.get_boolean_input()

            interface.print_("\n")
            if battle.fled:
                return namespace.BATTLE_FLED

            continue

        if command[0] == namespace.BATTLE_ATTACK:
            result =  battle.player_attack_phase()

            if result != namespace.BACK:
                return result
