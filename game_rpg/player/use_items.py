from ..items import CONSUMABLE
from .. import interface


def consume_items(self, items_to_consume, show_messages=True):
    if not isinstance(items_to_consume.attribute, CONSUMABLE):
        interface.centerprint(interface.get_messages("items.can't_be_consumed"))
        return False

    consume = {}
    for stats, values in items_to_consume.attribute.stats.items():
        if isinstance(values, dict):
            modiefer = getattr(self, values["modiefer"])
            values = int(values["value"] / 100 * modiefer)
        consume[stats] = values

    full = True
    full_stats = []
    for name in consume.keys():
        if getattr(self, name) == getattr(self, "max_" + name, 0):
            full_stats.append(name)
            full &= True
        else:
            full &= False

    if full and items_to_consume.attribute.type_ == "restore":
        interface.centerprint(interface.get_messages("player.messages.can_not_consumed_items").format(
            stats=interface.generate_readable_list(full_stats), name=items_to_consume.name))
        interface.get_enter()
        return False

    for stats, values in consume.items():
        prior_values = getattr(self, stats)
        setattr(
            self,
            stats,
            prior_values + values
        )

        if show_messages:

            if items_to_consume.attribute.type_ == "restore" and getattr(self, stats, 0) - prior_values > 0:
                interface.centerprint(
                    interface.get_messages("player.messages.item_consumed_restored").format(amount=getattr(self, stats, 0) - prior_values, value=stats)
                )
            elif items_to_consume.attribute.type_ == "increase":
                interface.centerprint(
                    interface.get_messages("player.messages.item_used_increased").format(stat=interface.get_messages(stats, stats), amount=values)
                )
    
    items_to_consume.amount -= 1
    if items_to_consume.amount < 1 and items_to_consume in self.inventory:
        self.inventory.remove(items_to_consume)

    return True
