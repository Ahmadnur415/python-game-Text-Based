from typing import Optional
from .. import interface


def equip_items_interface(self, item_to_equip, location: Optional[str] = None):
    if item_to_equip.class_item != "equippable":
        interface.print_(
            interface.get_messages("equipment.items_cant_use").format(item=item_to_equip.name)
        )
        interface.get_enter()
        interface.print_("")
        return

    location_to_equip = None
    if isinstance(item_to_equip.equip_location, list) and not location:
        if len(item_to_equip.equip_location) > 1:
            while True:
                interface.print_()
                interface.print_(
                    interface.get_messages("equipment.choise_locate_items").format(
                        name_items=item_to_equip.name, location=interface.generate_readable_list(item_to_equip.equip_location, True).replace("_", " ")
                    )
                )
                index = interface.get_input(
                    interface.get_messages("input_messages.choise_index").format(
                        index=f"1 - {len(item_to_equip.equip_location)}", other="C")
                )

                interface.print_("\n")
                if index == "c":
                    return

                if index in [str(i) for i in range(1, len(item_to_equip.equip_location) + 1)]:
                    location_to_equip = item_to_equip.equip_location[int(index) - 1]
                    break

        if len(item_to_equip.equip_location) == 1:
            location_to_equip = item_to_equip.equip_location[0]
    else:
        location_to_equip = item_to_equip.equip_location[0]
        if location:
            location_to_equip = location

    if location_to_equip in ("main_hand", "off_hand") and self.equipment['two_hand']:
        self.unequip_item("two_hand")

    if location_to_equip == "two_hand":
        self.unequip_item("main_hand")
        self.unequip_item("off_hand")

    item_use = self.equipment[location_to_equip]
    if item_use:
        interface.print_message("equipment.item_already_equipped", item=item_use.name)
        choise = interface.get_boolean_input()
        if not choise:
            return

        self.unequip_item(location_to_equip)
    return self.equip_item(item_to_equip, location_to_equip)
