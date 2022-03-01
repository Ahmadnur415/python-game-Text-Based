from .. import interface, namespace, util
from ..entity import DATA


def inventory_interface(self, class_item: str | None = None):

    while True:
        self.inventory_view(class_item)

        items_to_show = []
        for items in self.inventory:
            if not class_item or class_item == items.class_item:
                items_to_show.append(items)


        if not items_to_show:
            interface.get_enter()
            return

        command = interface.get_command(items_to_show, "Items", loop=False)

        if not isinstance(command, tuple):
            continue

        interface.print_("\n")
        if command[0] == namespace.BACK:
            return command[0]

        item = items_to_show[command[1] - 1]
        self.item_interface(item)


def consumable_interface(self, loop: bool = False):

    while True:
        self.inventory_view(namespace.CONSUMABLE)

        if not self.consumable_items:
            break

        command = interface.get_command(self.consumable_items, "Items", loop=False)

        if not isinstance(command, tuple):
            continue

        if command[0] == namespace.BACK:
            return namespace.BACK

        if 0 < command[1] < len(self.consumable_items) + 1:

            interface.print_("\n")

            items_to_use = self.consumable_items[command[1] - 1]
            result = self.consume_item(items_to_use)

            interface.print_("\n")

            if result and not loop:
                return result


def used_point_level_interface(self):
    while True:
        stats = DATA["values"]["basic"].copy()
        commands = [
            util.short_stat(name) + " : " + str(getattr(self, name)) for name in stats
        ]

        interface.print_title("Point Level")

        interface.print_message("player.point_level", "left", self.point_level)
        command = interface.get_command(commands, "Stat", list_option=True, loop=False)

        if not isinstance(command, tuple):
            continue

        interface.print_("\n")
        index = command[0]

        if index == namespace.BACK:
            return index

        stat = stats[command[1] - 1]

        if self.point_level < 1:
            interface.print_message( "player.not_enough_point" )
            interface.get_enter()
            continue

        break

    while True:
        interface.print_title("Point Level")
        interface.leftprint(
            stat.capitalize() + " " + str(getattr(self, stat)),
            " " * 4 + interface.get_messages("desc." + stat, stat),
            interface.get_messages("player.index_point_level").format(amount=self.point_level, stat=stat)
        )
        result_amount = interface.get_command([i for i in range(1, self.point_level+1)], loop=False)

        if not isinstance(result_amount, tuple):
            continue

        if result_amount[0] == namespace.BACK:
            return self.used_point_level_interface()

        self.point_level -= result_amount[0]
        setattr(self, stat, getattr(self, stat) + result_amount[0])
        interface.print_("")

        return self.used_point_level_interface()