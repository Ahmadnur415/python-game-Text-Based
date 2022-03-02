from .. import interface
from .data import DATA

def equip_item(self, item_to_equip, location: str):
    if item_to_equip.class_item != "equippable":
        interface.print_message("equipment.items_cant_use", item=item_to_equip.name)
        return

    if item_to_equip.used and item_to_equip not in self.equipment.values():
        for location in self.equipment.keys():
            if item_to_equip == self.equipment.get(location):
                pass

    self.equipment[location] = item_to_equip

    for _, stats in item_to_equip.stats.items():
        for stat, value in stats.items():

            if stat in DATA["values"]["resource"]:
                stat = "_max_" + stat

            if stat in DATA["values"]["critical"]:
                stat = "_" + stat

            if stat in DATA["full_stats"]:
                setattr(self, stat, getattr(self, stat) + value)

    item_to_equip.used = True
    item_to_equip.location_used = location
    if item_to_equip not in self.inventory:
        self.inventory.append(item_to_equip)


def unequip_item(self, location: str):
    items_to_unequip = self.equipment.get(location)

    if not items_to_unequip:
        return

    self.equipment[location] = None
    items_to_unequip.used = False
    items_to_unequip.location_used = None

    for _, stats in items_to_unequip.stats.items():
        for stat, value in stats.items():

            if stat in DATA["values"]["resource"]:
                stat = "_max_" + stat

            if stat in DATA["values"]["critical"]:
                stat = "_" + stat

            if stat in DATA["full_stats"]:
                setattr(self, stat, getattr(self, stat) - value)
