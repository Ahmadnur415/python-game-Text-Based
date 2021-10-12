from game_rpg import file
from pathlib import Path

GAME = None
DATA_ENTITY = None
DATA_ITEMS = None
SETTING = None
LANG = None
_ATTACK = None
_ENEMY = None


def _init():
    global GAME, DATA_ENTITY, DATA_ITEMS, SETTING, LANG, _ATTACK, _ENEMY
    GAME = file._init()
    DATA_ENTITY = GAME["entity"]
    DATA_ITEMS = GAME["items"]

    SETTING = GAME["setting"].copy()
    LANG = GAME["lang"].copy()
    _ATTACK = GAME["attack"]
    _ENEMY = GAME["enemy"]


# init game
_init()
Path("./saves/").mkdir(parents=True, exist_ok=True)

