from . import entity, until
from .setup import DATA_ENTITY, SETTING
from .player import inventory, view, attack
import random


class Enemy(entity.Entity):
    def __init__(
            self,
            name,
            _class,
            level,
            attacks,
            equipments,
            stats,
            looting=None
    ):
        super().__init__(
            name=name,
            namespace="Enemy",
            _class=_class,
            attacks=attacks,
            equipments=equipments,
            stats=stats['stats'],
            type_attack=stats["typeAttack"],
            style_attack=stats["styleAttack"]
        )

        if not looting:
            looting = []

        _generate_stats_enemy(self, stats.get("prority", []))
        self.level = level

        self.health = self.max_health
        self.mana = self.max_mana
        self.stamina = self.max_stamina
        self.looting = looting

    append_inventory = inventory.append_inventory
    view_equipment = view.view_equipment

    view_attack = attack.view_attack
    get_attack_from_name = attack.get_attack_from_name
    attack_name = attack.attack_name


def _generate_stats_enemy(enemy, priority_stats):
    change_data = create_change_data_stats(priority_stats)
    for i in range(1, enemy.level + 1):

        point = until.resolve_random_condition([
            (1, 45 - SETTING["difficulty"] * 5),
            (2, 35),
            (3, 20 + SETTING["difficulty"] * 5)
        ])

        for j in range(0, point):
            stats = until.resolve_random_condition(change_data)
            if not stats:
                stats = random.choice(DATA_ENTITY["stats"])
            value = getattr(enemy, stats, 0)

            if stats in DATA_ENTITY["entity_values"]["resource"]:
                setattr(enemy, stats, value + 3)
            else:
                setattr(enemy, stats, value + 1)


def create_change_data_stats(prority_stats: list):
    change_data = []

    priority_change = round(max(25 + (10 * len(prority_stats)), 65) / len(prority_stats), 2)

    non_priority_stats = DATA_ENTITY["stats"].copy()
    [non_priority_stats.remove(i) for i in prority_stats]
    non_priority_change = round((100 - priority_change) / len(non_priority_stats), 2)
    remainder = 100 - (priority_change * len(prority_stats) + non_priority_change * len(non_priority_stats))

    pre_non_priority_change = non_priority_change
    for stats in DATA_ENTITY["stats"]:
        non_priority_change = pre_non_priority_change
        if stats in prority_stats:
            change_data.append((stats, priority_change))
        else:
            if remainder < 1:
                non_priority_change += remainder
            change_data.append((stats, non_priority_change + remainder))

    return change_data