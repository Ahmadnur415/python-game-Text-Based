from .game import Game
from .. import interface, namespace, saveload

def enter(_, player):


    while True:
        commands = [namespace.ADVENTURE, namespace.SHOP, namespace.CAMP, namespace.SAVE_GAME, namespace.QUIT]

        interface.print_title("main_menu")
        result = interface.get_command(commands, add_command_back=False, loop=False, list_option=True)

        if not isinstance(result, tuple):
            continue

        interface.print_("\n")
        if result[0] == namespace.ADVENTURE:

            if player.health < int(0.2 * player.max_health):
                interface.print_message("player.cant_battle")
                interface.get_enter()
                continue

            from .adventure import main as adventure
            return adventure.enter(player)

        if result[0] == namespace.SHOP:
            from .shop import main as shop
            return shop.enter(player)

        if result[0] == namespace.CAMP:
            from .camp import main as camp
            return camp.enter(player)

        if result[0] == namespace.SAVE_GAME:
            result = saveload.save_game(player)
            if result:
                interface.print_message("game.saveload.saved")
                interface.get_enter()
            continue


        if result[0] == namespace.QUIT:
            quit()



main = Game(
    namespace.MAIN_MENU,
    enter
)