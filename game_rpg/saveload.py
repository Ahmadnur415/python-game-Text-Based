import os
import pickle
import glob
from datetime import datetime
from .player import Player
from . import interface, namespace, __version__

def save_game(player: Player):
    path = "./saves/"
    file_name = player.name + ".sv"
    i = 0

    while file_name in glob.glob(path + "*.sv"):
        file_name = f"{i+1} {player.name}.sv"
        i += 1

    with open(path + file_name, "wb") as f:
        pickle.dump(player, f, pickle.HIGHEST_PROTOCOL)

    return True

def load_game():
    lines = []
    line = interface.get_messages("game.saveload.line")
    interface.print_title("load_game")

    for filename in glob.glob("./saves/*.sv"):

        try:
            player = pickle.load(open(filename, "rb"))
        except ArithmeticError:
            continue

        if player.version != __version__ or not isinstance(player, Player):
            continue

        time = datetime.fromtimestamp(os.path.getmtime(filename)).strftime("%X %x")
        lines.append((player, time))

    if not lines:
        interface.leftprint( line.format( "No", "Name", "level", "Time" ), width=100 )
        interface.print_message("game.saveload.no_file_save")
        interface.get_enter()
        return False

    while lines:

        interface.leftprint(line.format( "No", "Name", "level", "Time" ), width=100)
        for i, values in enumerate(lines):
            interface.leftprint(
                line.format(i+1, values[0].name, values[0].level, values[1]), width=100
            )

        result = interface.get_command(lines, loop=False)

        if not isinstance(result, tuple):
            continue

        interface.print_("\n")
        if result[0] == namespace.BACK:
            return result[0]

        return result[0][0]
