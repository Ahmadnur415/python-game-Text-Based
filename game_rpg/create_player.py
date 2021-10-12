from .setup import DATA_ENTITY, GAME
from . import interface, player


_CLASSES = DATA_ENTITY["attribute"]["player_role"].copy()
def create_player():
    interface.centerprint(
        interface.get_messages("game.title.welcome"),
        interface.get_messages("game.title.input_name")
    )

    name_player = input(interface.get_messages("game.input_name"))
    if name_player in "":
        name_player = "PLayer"
    

    print()
    while True:
        interface.centerprint(
            interface.get_messages("game.title.index_role"),
            interface.get_messages("input_messages.choise_role_player").format(
                role=interface.generate_readable_list(_CLASSES, True)       
            )
        )
        
        index = interface.get_input()

        print()

        if index in [str(i) for i in range(1, len(_CLASSES) + 1)]:
            role = _CLASSES[int(index)-1]

            return player.Player(
                name=name_player,
                _class=role,
                attacks=[],
                
            )

def select_dificulty():
    interface.centerprint(
        interface.get_messages("game.title.index_dificulty"),
        interface.generate_readable_list(
            [f"{i+1}) {name}" for i, name in enumerate(GAME["difficulty"])]
        )
    )
    difficulty = interface.get_int_input(len(GAME["difficulty"]))
    return difficulty
