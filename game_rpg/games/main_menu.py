from .. import interface
from .game import game as GAME


def enter(self, game):
    rooms = self.commands.copy()
    rooms.append("exit")

    while True:
        interface.centerprint(interface.get_messages("game.title"), "-- " + str(self.name.upper()) + " --")
        for i, room in enumerate(rooms):
            interface.leftprint(f"({i + 1}) {str(room).capitalize().replace('_', ' ')}")
        
        index = interface.get_int_input(len(rooms)) - 1
        print()

        next_rooms = rooms[index]
        if next_rooms == "exit":
            return "exit"
        
        if next_rooms in self.commands:
            return next_rooms

main = GAME(
    "main menu",
    enter=enter
)