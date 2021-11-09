from game_rpg import file
from pathlib import Path


def _init():
    global GAME, DATA_ENTITY, DATA_ITEMS, SETTING, LANG, _ATTACK
    GAME = file._init()
    DATA_ENTITY = GAME["entity"]
    DATA_ITEMS = GAME["items"]

    SETTING = GAME["setting"].copy()
    LANG = GAME["lang"].copy()
    _ATTACK = GAME["attack"]
    Path("./saves/").mkdir(parents=True, exist_ok=True)

# init game
_init()
