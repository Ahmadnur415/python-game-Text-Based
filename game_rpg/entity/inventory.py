from .. import interface

def add_items(self, *items):
    for item in items:
        if not item:
            continue
        if not self.inventory or item.class_item == "equippable":
            self.inventory.append(item)

        elif item.class_item == "consumable":
            for item_in_inventory in self.inventory:
                if item_in_inventory.identify == item.identify:
                    item_in_inventory.amount += item.amount
                    break
            else:
                self.inventory.append(item)


def remove_items(self, *items):
    for item in items:
        if item in self.inventory:

            if item.used:
                interface.print_message("item.cant_remove")
                interface.get_enter()
                continue

            self.inventory.remove(item)

@property
def equippable_items(self):
    items = []
    for item in self.inventory:
        if item.class_item == "equippable":
            items.append(item)

    return items


@property
def consumable_items(self):
    items = []
    for item in self.inventory:
        if item.class_item == "consumable":
            items.append(item)
    return items
