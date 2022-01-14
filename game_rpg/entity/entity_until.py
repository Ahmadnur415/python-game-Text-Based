from ..setup import ENTITY


def _make_of_equipment():
    equipment = []
    for _, locate_equip in ENTITY["attribute"]["equipment"].items():
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


ENTITY["equipment"] = _make_of_equipment()