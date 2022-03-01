from .. import interface

def _generate_value_entity(name):

    @property
    def value_property(entity):

        if getattr(entity, "_" + name) > getattr(entity, "max_" + name):
            setattr(entity, "_" + name, getattr(entity, "max_" + name))

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

def generate_missing_value_property(name):

    @property
    def value_property(entity):
        return getattr(entity, "max_" + name) - getattr(entity, name)

    @value_property.setter
    def value_property(entity, value):
        pass

    return value_property

def generate_exp_value_property():

    @property
    def value_property(entity):
        return getattr(entity, "_exp")

    @value_property.setter
    def value_property(entity, value):
        value_max = getattr(entity, "max_exp")

        if value < 0:
            value = 0

        setattr(entity, "_exp", value)


        if entity.exp > value_max and entity.level < entity.max_level:

            entity.level += 1
            interface.centerprint(
                interface.get_messages("player.level_up").format(entity.level), width=entity.message_width_for_lv
            )

            entity.point_level += 3

            entity.health = entity.max_health
            entity.mana = entity.max_mana
            entity.stamina = entity.max_stamina

            entity.exp -= value_max

    return value_property

