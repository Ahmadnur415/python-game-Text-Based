from game_rpg import namespace, interface
from game_rpg.create_player import create_player, Player
from game_rpg.saveload import load_game
from pathlib import Path


def play():
    while True:
        interface.print_title("welcome")

        index = interface.get_command([namespace.PLAY, namespace.LOAD, namespace.QUIT], add_command_back=False, loop=False, list_option=True)

        interface.print_("\n")
        match index[0]:

            case namespace.LOAD:
                result = load_game()

                if isinstance(result, Player):
                    from game_rpg.games import camp
                    return camp.enter(result)

                continue

            case namespace.PLAY:
                return create_player()

            case namespace.QUIT:
                return quit()


if __name__ == "__main__":
    Path("./saves/").mkdir(parents=True, exist_ok=True)
    play()
