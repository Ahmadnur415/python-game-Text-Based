from game_rpg.setup import DATA_ENTITY, DATA_ITEMS
from .. import interface


def equip_items(self, items, location=None, append_inventory=False):
    if items.namespace != "EQUIPPABLE" or not items.attribute.location and not location:  # or items.attribute.location not in setup.DATA_ENTITY["attribute"]["equipment"]:
        interface.print_(interface.get_messages("equipment.items_cant_use").format(item=items.name))
        return

    location = None if location not in items.attribute.location else location
    location_equipment: str = ""

    if "two_hand" in items.attribute.location:
        for names in ("main_hand", "off_hand"):
            items_equip = self.equipment[names]
            if items_equip:
                self.unequip_items(names)

    if isinstance(items.attribute.location, list) and not location:
        if len(items.attribute.location) > 1:
            while True:
                print()
                print(
                    interface.get_messages("equipment.choise_locate_items").format(
                        name_items=items.name, location=interface.list_line(
                            items.attribute.location, number=True, replace=("_", " ")
                        )
                    )
                )
                # index = interface.get_input(f"[1 - {len(items.attribute.location)} | c]")
                index = interface.get_input(
                    interface.get_messages("input_messages.choise_index").format(
                        index=f"1 - {len(items.attribute.location)}", other="C")
                )

                if index == "c":
                    return 
                if index in [str(i) for i in range(1, len(items.attribute.location) + 1)]:
                    location_equipment = items.attribute.location[int(index) - 1]
                    break

        if len(items.attribute.location) == 1:
            location_equipment = items.attribute.location[0]
    else:
        location_equipment = items.attribute.location
        if location:
            location_equipment = location

    # remove equipment two_hand if location_equipment in ("main_hand", "off_hand")
    if location_equipment in ("main_hand", "off_hand") and self.equipment['two_hand']:
        self.unequip_items("two_hand")

    # == proses:
    # Overide items
    item_use = self.equipment[location_equipment]
    if item_use:
        interface.print_(
            interface.get_messages("equipment.item_already_equipped").format(
                item=item_use.name
            )
        )
        choise = interface.get_boolean_input()
        if not choise:
            return 
            
        self.unequip_items(location_equipment)

    # fix bug 1 items tapi terpasang di 2 lokasi
    if items.attribute.use:  # and isinstance(items.attribute.location, list):
        for locate in self.equipment.keys():
            if items == self.equipment.get(locate):  # same equipment
                self.unequip_items(locate)

    # Equip items
    self.equipment[location_equipment] = items

    # Add stats Items
    for stats, value in items.sub_stats.items():
        if stats in DATA_ENTITY["entity_values"]["resource"]:
            setattr(self, "_max_" + stats, getattr(self, "_max_" + stats) + value)
            continue
        
        if stats in ["critical_change" , "critical_hit"]:
            continue

        setattr(self, stats, getattr(self, stats) + value)

    # add primary stats
    for stats in DATA_ITEMS["attribute"]["basic"]:
        value = getattr(items.attribute, stats, None)
        # print(stats, value)
        if stats != "damage" and value:
            setattr(self, stats, getattr(self, stats) + value)
    
    # Add attack
    if location_equipment in ("main_hand", "two_hand"):
        for attack in items.attribute.attack:
            self.attack.append(attack)

    items.attribute.use = True
    if append_inventory:
        self.append_inventory(items)

    # fix bug
    for stats in DATA_ENTITY["entity_values"]["resource"]:
        if getattr(self, stats) > getattr(self, "max_" + stats):
            setattr(self, stats, getattr(self, "max_"+stats))

    return 


def unequip_items(self, locate_items):
    items_to_unequip = self.equipment.get(locate_items)

    if not items_to_unequip:
        return

    self.equipment[locate_items] = None
    items_to_unequip.attribute.use = False

    # remove attack
    for attack in items_to_unequip.attribute.attack:
        if attack in self.attack:
            self.attack.remove(attack)

    # remove sub stats
    for stats, value in items_to_unequip.sub_stats.items():
        if stats in DATA_ENTITY["entity_values"]["resource"]:
            setattr(self, "_max_" + stats, getattr(self, "_max_" + stats) - value)
            if getattr(self, stats) > getattr(self, "_max_" + stats):
                setattr(self, stats, getattr(self, "_max_" + stats))
            continue
        
        if stats in ["critical_change" , "critical_hit"]:
            continue

        setattr(self, stats, getattr(self, stats) - value)

    # remove primary stats
    for stats in DATA_ITEMS["attribute"]["basic"]:
        value = getattr(items_to_unequip.attribute, stats, None)
        if stats != "damage" and value:
            setattr(self, stats, getattr(self, stats) - value)