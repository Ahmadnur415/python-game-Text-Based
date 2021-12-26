from pathlib import Path
from game_rpg import file

global GAME, DATA_ENTITY, DATA_ITEMS, SETTING, LANG, _ATTACK


class setup:
    def __init__(self):
        self.refresh()

    @property    
    def data_entity(self):
        return self.Game["entity"]

    @property
    def data_Items(self):
        return self.Game["items"]
    
    @property
    def lang(self):
        return file._load_lang(self.Game['fileGame']["lang"])

    @property
    def _attack(self):
        return self.Game["attack"]

    def refresh(self):
        self.Game = file._load("game.data.json")
        self.Game["items"].update(file._load_items())
        self.Game["entity"] = file._load_entity(self.Game["fileGame"]["entity"])
        self.Game["attack"] = file._load(self.Game["fileGame"]["attack"])

_setup = setup()

GAME = _setup.Game
DATA_ENTITY = _setup.data_entity
DATA_ITEMS = _setup.data_Items
LANG = _setup.lang
_ATTACK = _setup._attack

SETTING = GAME["setting"].copy()
Path("./saves/").mkdir(parents=True, exist_ok=True)
