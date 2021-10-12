from .. import interface
from ..room import Room


VIEW = "view player"
INV = "Inventory"
EQU = "equipment"
SAVE = "save game"


def enter(self, game):
    commands = [VIEW, INV, EQU, SAVE]
    commands.extend(self.commands.copy())

    while True:
        
        interface.centerprint("-- "+interface.get_messages("game.title") + " --", "-- " + str(self.name.upper()) + " --")

        for i, room in enumerate(commands):
            interface.leftprint(f"({i + 1}) {str(room).capitalize().replace('_', ' ')}")
        
        index = interface.get_int_input(len(commands)) - 1
        # New Line
        print()

        index = commands[index]
        if index == VIEW:
            result = game.player.view_stats_interface()
            if result == "back":
                continue            

        if index == INV:
            game.player.view_inventory_interface()
            
        if index == EQU:
            game.player.view_equipment()
            interface.get_enter()

        if index == SAVE:
            game.save_game()
            interface.centerprint(interface.get_messages("game.saved"))
            interface.get_enter()
            continue

        if index in self.commands:
            return index


ROOM = Room(
    name="camp",
    enter=enter
)