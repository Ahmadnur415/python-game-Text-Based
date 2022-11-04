from game_rpg import __version__
from . import equipment, view, consume_item, player_interface, item_interface
from .. import entity, data
from ..item import get_items

DATA = data._load("player.json")


class Player(entity.Entity):
    def __init__(self, name: str, _class : str, dificulty: int = 1):
        DataPlayer = DATA.get(_class)
        if not DataPlayer:
            raise ()

        super().__init__(
            namespace = self.__class__.__name__,
            equipments = DataPlayer["equipment"],
            stats = DataPlayer["stats"],
            type_damage = DataPlayer["type_damage"]
        )

        for name in entity.DATA["player_values"]:
            if isinstance(name, list):
                setattr(self, name[0], name[1])
                continue
            setattr(self, name, None)

        for item in DataPlayer["inventory"]:
            self.add_items(get_items(item["id"], item["value"]))

        self.version = __version__
        self._class = _class
        self.__name = name
        self.__dificulty = dificulty        
        
        self.health = self.max_health
        self.mana = self.max_mana
        self.stamina = self.max_stamina
        

    @property
    def name(self):
        return self.__name

    @property
    def dificulty(self):
        return self.__dificulty

    equip_items_interface =  equipment.equip_items_interface
    inventory_view = view.inventory_view
    equipment_view = view.equipment_view
    attacks_view = view.attacks_view
    view = view.player_view
    consumable_interface = player_interface.consumable_interface
    inventory_interface = player_interface.inventory_interface
    used_point_level_interface = player_interface.used_point_level_interface
    consume_item = consume_item.consume_item
    sell_item = item_interface.sell_item
    item_interface = item_interface.item_interface
