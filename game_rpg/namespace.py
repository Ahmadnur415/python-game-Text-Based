INVENTORY = "Inventory"
EQUIPMENT = "Equipment"
USE_ITEMS = "Use item"
SAVE_GAME = "Save game"
CONSUME_ITEMS = "Consume item"
REMOVE_ITEMS = "Unequip item"
SELL_ITEMS = "Sell item"
VIEW_ATTACK = "View attack"
VIEW_STATS = "View stat"
POINT_LEVEL = "Point level"

EQUIPPABLE = "equippable"
CONSUMABLE = "consumable"

MAIN_MENU = "main menu"
ADVENTURE = "adventure"
CAMP = "camp"
SHOP = "shop"
DUNGEONS = "dungeons"

PLAY = "Play"
LOAD = "Load"
QUIT = "Quit"
BACK = "Back"

EASY = "easy"
MEDIUM = "medium"
HARD = "hard"

NAME = "name"
PRICE = "price"
QUALITY = "quality"

BATTLE_ATTACK =  "attack"
BATTLE_FLED = "fled"
BATTLE_WIN = "win"
BATTLE_LOSE = "lose"
LOOT = "loot"

COMMON = "common"
UNCOMMON = "uncommon"
RARE = "rare"
EPIC = "epic"
LEGENDARY = "legendary"
SPECIAL = "special"

LIST_OF_QUALITY = [ COMMON, UNCOMMON, RARE, EPIC, LEGENDARY, SPECIAL ]
COMMANDS_PLAYER = [VIEW_STATS, INVENTORY, EQUIPMENT, POINT_LEVEL, VIEW_ATTACK, SAVE_GAME]


class TYPE_ATTACK:
    # 1.5 / 8 stat
    MELEE = "strength"
    RANGED = "perception"
    SHORT_MELEE = "dextery"
    SPEEL = "will"
    MAGIC = "magic"
    SHIELD = "constitution"

class DIRECTION:
    NORTH = "north"
    SOUTH = "south"
    WEST = "west"
    EAST = "east"
