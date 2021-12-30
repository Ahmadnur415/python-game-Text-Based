from ..setup import ENTITY
from . import other_property, attack, entity_until, equipment, view


class Entity:
    def __init__(
        self,
        name: str = "Entity",
        namespace: str = "entity",
        _class=None,
        attacks: list = None,
        equipments: dict = None,
        stats: dict = None,
        type_attack=None,
        style_attack=None
    ):

        if not stats:
            stats = {}

        for names, value in stats.items():
            if names in ENTITY["entity_values"]["resource"]:
                names = "_max_" + names
            setattr(self, names, value)

        for stat in ENTITY["all_stats"]:
            if not hasattr(self, stat):
                setattr(self, stat, 0)

        if attacks is None:
            attacks = []

        if equipments is None:
            equipments = {}

        self.__name = name
        self.__namespace = namespace.lower()
        self.__class = _class
        self.level = 1
        self.equipment = dict.fromkeys(ENTITY["equipment"])
        self.inventory = []
        self.attack = attacks
        self.type_attack = type_attack
        self.style_attack = style_attack

        self.health = self.max_health
        self.mana = self.max_mana
        self.stamina = self.max_stamina
        
        for locate, item_to_equip in equipments.items():
            self.equip_items(item_to_equip, locate, True)

    @property
    def name(self):
        return self.__name

    @property
    def _class(self):
        return self.__class

    @property
    def namespace(self):
        return self.__namespace

    max_health = other_property.max_health
    max_mana = other_property.max_mana
    max_stamina = other_property.max_stamina

    critical_change = other_property.critical_change
    critical_hit = other_property.critical_hit

    reduce_damage = other_property.reduce_damage
    magic_damage = other_property.magic_damage
    physical_damage = other_property.physical_damage
    evaded = other_property.evaded
    damage = other_property.damage

    attack_state = attack.attack_state
    usable_attacks = attack.usable_attacks
    attack_turn_count = attack.attack_turn_count

    equip_items = equipment.equip_items
    unequip_items = equipment.unequip_items

    view_stats = view.view_stats


# create health 
for name in ENTITY["entity_values"]["resource"]:
    setattr(
        Entity,
        name,
        entity_until._generate_value_property(name)
    )
