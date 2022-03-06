from .data import DATA
from . import attack_state, other_property, util, equipment, inventory
from .. import item


class Entity:
    def __init__(
        self,
        namespace: str,
        attacks: str | None = None, 
        equipments: dict | None = None,
        stats: dict | None = None,
        type_damage: str | None = None
    ):
        
        if not attacks:
            attacks = []

        if not stats:
            stats = {}
                
        for name, values in stats.items():
            for stat, value in values.items():
                if name == "resource":
                    stat = "_max_" + name
                
                if name == "critical":
                    stat = "_" + stat

                if stat in DATA["full_stats"]:
                    setattr(self, stat, value)
        
        for stat in DATA["stats"]:
            if not hasattr(self, stat):
                setattr(self, stat, 0)
        
        for name in DATA["entity_values"]:
            if isinstance(name, list):
                setattr(self, name[0], name[1])
                continue
            setattr(self, name, None)

        self._namespace = namespace
        self._attacks = attacks
        self.inventory = []
        self.equipment = DATA["full_equipment"].copy()       
        self.type_damage = type_damage

        for location, item_to_equip in equipments.items():
            if isinstance(item_to_equip, str):
                item_to_equip = item.get_items(item_to_equip)
            self.equip_item(item_to_equip, location)

        self.health = self.max_health
        self.mana = self.max_mana
        self.stamina = self.max_stamina

    max_level = DATA["max_level"]
    max_health = other_property.max_health
    max_mana = other_property.max_mana
    max_stamina = other_property.max_stamina
    critical_change = other_property.critical_change
    critical_damage = other_property.critical_damage
    reduce_damage = other_property.attack_reduce
    physical_attack_reduce = other_property.physical_attack_reduce
    magic_attack_reduce = other_property.magic_attack_reduce
    max_exp = other_property.max_exp
    evaded = other_property.evaded
    usable_attacks = other_property.usable_attacks
    attacks = other_property.attacks
    equip_item = equipment.equip_item
    unequip_item = equipment.unequip_item
    add_items = inventory.add_items
    remove_items = inventory.remove_items
    equippable_items = inventory.equippable_items
    consumable_items = inventory.consumable_items
    attack_state = attack_state.attack_state
    update = util.update

 
for name in DATA["values"]["resource"]:
    setattr(
        Entity, name, util._generate_value_entity(name)
    )

    setattr(
        Entity, "missing_" + name, util.generate_missing_value_property(name)
    )

setattr(
    Entity, "exp", util.generate_exp_value_property()
)
