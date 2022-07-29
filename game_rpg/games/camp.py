from .game import Game
from .. import interface, namespace, saveload


def enter(_, player):
    while True:

        interface.print_title(namespace.CAMP)

        POINT_PLAYER = namespace.POINT_LEVEL + (" (+)" if player.point_level > 0 else "")
        commands = namespace.COMMANDS_PLAYER.copy()
        if commands.index(namespace.POINT_LEVEL):
            commands[commands.index(namespace.POINT_LEVEL)] = POINT_PLAYER

        result = interface.get_command(commands, list_option=True, loop=False)
        if not isinstance(result, tuple):
            continue

        interface.print_("\n")

        if result[0] == namespace.BACK:
            from .main import main as main_menu
            return main_menu.enter(player)

        elif result[0] == namespace.VIEW_STATS:
            interface.print_title("stats_player")
            player.view()
            interface.get_enter()
            continue

        elif result[0] == namespace.INVENTORY:
            player.inventory_interface()
            continue

        elif result[0] == namespace.EQUIPMENT:
            player.equipment_view()
            interface.get_enter()
            continue


        elif result[0] == namespace.VIEW_ATTACK:
            player.attacks_view()
            interface.get_enter()
            continue

        elif result[0] == namespace.SAVE_GAME:
            result = saveload.save_game(player)
            if result:
                interface.print_message("game.saveload.saved")
                interface.get_enter()
            continue

        elif result[0] == POINT_PLAYER:
            player.used_point_level_interface()
            continue


main = Game(
    namespace.CAMP,
    enter
)