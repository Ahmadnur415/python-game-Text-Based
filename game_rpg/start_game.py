from . import interface, game, namespace

commands = [namespace.PLAY, namespace.LOAD, namespace.QUIT]


def start_game():
    while True:
        interface.centerprint(interface.get_messages("game.title.welcome"))

        for i, command in enumerate(commands):
            interface.leftprint(f"({i+1}) {command}")
        interface.centerprint('-')

        index = interface.get_input()
        try:
            index = commands[int(index) - 1]
        except (ValueError, IndexError):
            continue

        print()
        if index == namespace.PLAY:
            return game.Game().start()

        if index == namespace.LOAD:
            result_load = game.load_game()
            
            if isinstance(result_load, game.Game):
                return result_load.start()

            continue

        if index == namespace.QUIT:
            return quit()
