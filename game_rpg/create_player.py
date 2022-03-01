from .data import _load
from . import interface, namespace
from .player import Player, DATA


dt_role = list(DATA.keys())


def create_player():

    name = ""
    while len(name) < 8:
        interface.print_title("welcome")
        interface.print_title("input_name")

        name = input(interface.get_messages("input_messages.input_name"))

        interface.print_("\n")
        if len(name) > 8:
            break

        interface.print_message("input_messages._name")
        interface.print_("\n")



    while True:
        interface.print_title("welcome")
        interface.print_title("index_role")
        index = interface.get_command(dt_role, add_command_back=False, loop=False, list_option=True)

        if not isinstance(index, tuple):
            continue

        role = index[0]
        break

    interface.print_("\n")
    while True:
        interface.print_title("welcome")
        interface.print_title("index_dificulty")

        index = interface.get_command([namespace.EASY, namespace.MEDIUM, namespace.HARD], "dificulty", add_command_back=False, loop=False, list_option=True)

        if not isinstance(index, tuple):
            continue

        dificulty = index[1]
        break

    interface.print_("\n")
    player = Player( name, role, dificulty )

    from .games import main_menu
    return main_menu.enter(player)
