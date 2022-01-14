from pathlib import Path
from game_rpg import file

global GAME, ENTITY, ITEMS, SETTING, LANG, _ATTACK


class setup:
    def __init__(self):
        self.load_data()

    @property    
    def data_entity(self):
        return self.Game["entity"]

    @property
    def data_Items(self):
        return self.Game["items"]

    def lang(self):
        return file._load_lang(self.Game['fileGame']["lang"])

    def attack(self, name):
        return self.Game["attack"].get(name, None)

    def load_data(self):
        self.Game = file._load("game.data.json")
        self.Game["items"].update(file._load_items())
        self.Game["entity"] = file._load_entity(self.Game["fileGame"]["entity"])
        self.Game["attack"] = file._load(self.Game["fileGame"]["attack"])

    def enemy(self):
        return file._load(self.Game["fileGame"]["enemy"])


_setup = setup()
GAME = _setup.Game
ENTITY = _setup.data_entity
ITEMS = _setup.data_Items
LANG = _setup.lang
ATTACK = _setup.attack
ENEMY = _setup.enemy

SETTING = GAME["setting"].copy()
Path("./saves/").mkdir(parents=True, exist_ok=True)
