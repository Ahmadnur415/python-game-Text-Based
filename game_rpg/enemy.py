from .entity import Entity, DATA
from . import util
import random


class Enemy(Entity):
    def __init__(
        self,
        name: str,
        attacks: list,
        equipments: dict,
        stats: dict,
        type_damage: str,
        looting: list,
        level: int,
        inventory: list | None = None,
    ):

        super().__init__(
            namespace = self.__class__.__name__,
            attacks = attacks,
            equipments = equipments,
            stats = stats,
            type_damage = type_damage
        )

        if not looting:
            looting = []

        if not inventory:
            inventory = []

        if level > self.max_level:
            level = self.max_level

        self.name = name
        self.looting = looting
        self.level = level
        self.inventory.extend(inventory)

        _generate_stats_enemy(self)

        self.health = self.max_health
        self.mana = self.max_mana
        self.stamina = self.max_stamina


def _generate_stats_enemy(enemy: Enemy):
    for _ in range(enemy.level + 1):
        basic_stat = util.resolve_random_condition([
            ("basic", 60),
            ("defend", 20),
            ("resource", 15),
            ("critical", 5)
        ])

        point = util.resolve_random_condition( [ (2, 45), (3, 35), (1, 20) ] )

        stat = random.choice(DATA["values"][basic_stat].copy())

        if basic_stat == "critical":
            point = round(point / 0.5, 2) if stat == "critical_change" else round(point * 3.5)
            stat = "_" + stat

        if basic_stat == "resource":
            point = int(point * 2) if stat == "health" else int(point * 1.5)
            stat = "_max_" + stat

        setattr( enemy, stat, getattr(enemy, stat) + point )
