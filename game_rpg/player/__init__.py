from .. import entity, setup
from . import inventory, view, attack, player_interface, use_items, level
from ..attack import Attack
from ..items import get_items, Items as ITEMS

class Player(entity.Entity):
    def __init__(self, name, _class, attacks=None):
        DATA = setup.ENTITY["class"][_class].copy()
        equipment = {}

        if not attacks:
            attacks = []
        
        attacks.extend([
            Attack.load_attack(get_attack)
            for get_attack in DATA["attack"].copy()
            if DATA.get("attack", None)
        ])

        for names, id_items in DATA['equipment'].items():
            items = get_items(id_items)
            if isinstance(items, ITEMS):
                equipment[names] = items

        for stat, value in setup.ENTITY["player_values"].items():
            setattr(self, stat, value)

        super().__init__(
            name,
            namespace="player",
            _class=_class,
            attacks=attacks,
            equipments=equipment,
            stats=DATA["stats"],
            type_attack=DATA["type_damage"],
            style_attack=DATA["style_attack"]
        )
        
        self.health = self.max_health
        self.mana = self.max_mana
        self.stamina = self.max_stamina

        for items in DATA.get("inventory", []):
            self.append_inventory(get_items(items["id"], items["amount"]))
    max_exp = entity.other_property.max_exp

    consume_items = use_items.consume_items
    append_inventory = inventory.append_inventory
    
    equippable_items = inventory.equippable_items
    consumable_items = inventory.consumable_items
    view_inventory_interface = player_interface.view_inventory_interface
    view_stats_interface = player_interface.view_stats_interface
    items_interface = player_interface.items_interface
    use_items_consumable_interface = player_interface.use_items_consumable_interface
    point_level_interface = player_interface.point_level_interface

    # view
    view_inventory = view.view_inventory
    view_equipment = view.view_equipment
    view_attack = attack.view_attack

    get_attack_from_name = attack.get_attack_from_name
    attack_name = attack.attack_name

    levelUp = level.levelUp
    gain_exp = level.gain_exp