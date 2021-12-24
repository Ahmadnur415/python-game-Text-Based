from .. import entity, setup as init
from . import inventory, view, attack, player_interface, use_items, level
from ..attack import ATTACK
from ..items import get_items, Items as ITEMS

class Player(entity.Entity):
    def __init__(
        self,
        name, 
        _class, 
        attacks=None
    ):
        DATA = init.DATA_ENTITY["class"][_class].copy()

        if not attacks:
            attacks = []
        
        attacks.extend(
            [ATTACK(get_attack) for get_attack in DATA["attack"].copy() if DATA.get("attack", None)]
        )

        equipment = {}
        for names, id_items in DATA['equipment'].items():
            items = get_items(id_items)
            if not isinstance(items, ITEMS):
                continue
            equipment[names] = items

        super().__init__(
            name,
            namespace="player",
            _class=_class,
            attacks=attacks,
            equipments=equipment,
            stats=DATA["stats"],
            type_attack=DATA["typeAttack"],
            style_attack=DATA["styleAttack"]
        )
        
        for stat, value in init.DATA_ENTITY["player_values"].items():
            setattr(self, stat, value)
        
        self.health = self.max_health
        self.mana = self.max_mana
        self.stamina = self.max_stamina

        if self._class != "mage":
            self.append_inventory(get_items("potion.potions/recover_potion", 5))
        else:
            self.append_inventory(get_items("potion.potions/blue_potion", 5))

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