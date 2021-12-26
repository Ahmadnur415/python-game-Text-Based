from .. import interface, namespace
from .game import game as GAME


def enter(self, game):
    commands = [namespace.VIEW_PLAYER, namespace.INVENTORY, namespace.EQUIPMENT, namespace.SAVE_GAME]
    commands.extend(self.commands.copy())

    while True:
        
        interface.centerprint("-- "+interface.get_messages("game.title") + " --", "-- " + str(self.name.upper()) + " --")

        for i, room in enumerate(commands):
            interface.leftprint(f"({i + 1}) {str(room).capitalize().replace('_', ' ')}")
        
        index = interface.get_int_input(len(commands)) - 1
        print()

        index = commands[index]
        if index == namespace.VIEW_PLAYER:
            result = game.player.view_stats_interface()
            if result == namespace.BACK:
                continue            

        if index == namespace.INVENTORY:
            game.player.view_inventory_interface()
            
        if index == namespace.EQUIPMENT:
            game.player.view_equipment()
            interface.get_enter()

        if index == namespace.SAVE_GAME:
            game.save_game()
            interface.centerprint(interface.get_messages("game.saved"))
            interface.get_enter()
            continue

        if index in self.commands:
            return index

main = GAME(
    name="camp",
    enter=enter
)