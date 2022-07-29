from .. import interface, entity, util


def view(battle):
    interface.print_title("battle", battle.width_line)

    for name in interface.get_messages("battle.view"):
        print_line(battle, name)


def print_line(battle, stat):

    def get_value(ENTITY: entity.Entity):

        _value = getattr(ENTITY, stat)

        if stat in entity.DATA["values"]["resource"]:
            _value = str(
                    getattr( ENTITY, ("max_" if ENTITY._namespace != "Enemy" else "") + stat, stat)
                ) + " / " +  str(
                    getattr( ENTITY, ("max_" if ENTITY._namespace == "Enemy" else "") + stat, stat)
                )

        if stat in entity.DATA["values"]["critical"] or stat == "armor_penetration":
            _value = str(_value) + "%"

        return _value

    interface.printtwolines(
        "{:<8} : {}".format(util.short_stat(stat), get_value(battle.player)),
        "{} : {:>8}".format(get_value(battle.enemy), util.short_stat(stat)),
        width=int(battle.width_line/2)
    )
