from pydantic.dataclasses import dataclass

from ..stats import Stats
from . import other_properties
from .generate_value_property import (
    generate_exp_property,
    generate_level_property,
    generate_missing_value_property,
    generate_point_level_property,
    generate_value_property,
)


@dataclass
class EntityStats(Stats):
    point_level = generate_point_level_property()
    level = generate_level_property()
    exp = generate_exp_property()

    max_health = other_properties.max_health
    max_stamina = other_properties.max_stamina
    max_mana = other_properties.max_mana

    critical_change = other_properties.critical_change
    critical_damage = other_properties.critical_damage

    reduce_damage = other_properties.reduce_damage
    physical_attack_reduce = other_properties.physical_attack_reduce
    magic_attack_reduce = other_properties.magic_attack_reduce

    evaded = other_properties.evaded

    health = generate_value_property("health")
    mana = generate_value_property("mana")
    stamina = generate_value_property("stamina")

    missing_health = generate_missing_value_property("health")
    missing_mana = generate_missing_value_property("mana")
    missing_stamina = generate_missing_value_property("stamina")

    def __post_init__(self):
        self.health = self.max_health
        self.mana = self.max_mana
        self.stamina = self.max_stamina

    @property
    def max_level(self) -> int:
        """level max entity"""
        return 60
