from ..setup import DATA_ENTITY as DATA


def _full_list_of_stats():
    list_of_stats: list = []
    for _, name in DATA["entity_values"].items():
        list_of_stats.extend(name)
    
    list_of_stats.extend(
        ["_max_" + name for name in DATA["entity_values"]["resource"]]
    )
    return list_of_stats


def _make_of_equipment():
    equipment = []
    for _, locate_equip in DATA["attribute"]["equipment"].items():
        equipment.extend(locate_equip)

    return equipment


def _generate_value_property(name):
    @property
    def value_property(entity):
        return getattr(entity, "_" + name)

    @value_property.setter
    def value_property(entity, value):
        value_max = getattr(entity, "max_" + name)

        if value > value_max:
            value = value_max

        if value < 0:
            value = 0

        setattr(entity, "_" + name, value)

    return value_property


# DATA["stats"] = _full_list_of_stats()
DATA["equipment"] = _make_of_equipment()