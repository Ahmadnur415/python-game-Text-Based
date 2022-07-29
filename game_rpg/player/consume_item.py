from ..entity import DATA
from .. import namespace, interface, util


def consume_item(self, item_to_consume):
    if item_to_consume.class_item != namespace.CONSUMABLE:
        interface.centerprint(interface.get_messages("item.can't_consume"))
        return

    stats = {}
    for stat, value in item_to_consume.effects["stats"].items():
        if isinstance(value, dict):
            value = util._generate_value_from_dict(value, self, self)

        if isinstance(value, (int, float)):
            stats[stat] = int(value)


    full_stats = True
    if item_to_consume.effects["type"] == "restore":
        names = []
        for stat, value in stats.items():
            if getattr(self, stat) != getattr(self, "max_" + stat):
                full_stats = False
                break

            names.append(stat)
        if full_stats:
            interface.print_message(
                "player.messages.can_not_consumed_items", stats=interface.generate_readable_list(names), name=item_to_consume.name
            )

            return

    for stat, value in stats.items():
        prior_value = getattr(self, stat)
        setattr( self, stat, prior_value + value )
        if stat in DATA["values"]["resource"]:
            restore_value = getattr(self, stat) - prior_value
            if restore_value != 0:
                interface.print_message("player.messages.item_consumed_restored", value=restore_value, stat=stat)
            continue
        interface.print_message("player.messages.item_used_increased", stat=stat, value=prior_value)

    item_to_consume.amount -= 1
    if item_to_consume in self.inventory and item_to_consume.amount < 1:
        self.inventory.remove(item_to_consume)

    return True
