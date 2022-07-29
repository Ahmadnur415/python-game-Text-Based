from typing import Optional
from ..entity import DATA
from .. import interface, namespace, util


def inventory_view(self, class_item: Optional[str] = None):
    items_to_show = []
    for items in self.inventory:
        if not class_item or class_item == items.class_item:
            items_to_show.append(items)

    interface.print_title(("inventory" if not class_item else class_item))
    interface.leftprint(
        interface.get_messages("item.line_item").format(
            "No", interface.readable_item("", ("name", "quality", "type_item")).replace("_", " ")
        ), width=100
    )

    for i, inventory_item in enumerate(items_to_show):
        interface.leftprint(
            interface.get_messages("item.line_item").format(
                i + 1, interface.readable_item(inventory_item, ("name", "quality", "type_item"))
            ), width=100
        )

    if not self.inventory:
        interface.centerprint(interface.get_messages("inventory.no_have_items"), width=63)
        return

    elif class_item == namespace.EQUIPPABLE and not self.equippable_items:
        interface.centerprint(interface.get_messages("inventory.no_equippable_items"), width=63)
        return

    elif class_item == namespace.CONSUMABLE and not self.consumable_items:
        interface.centerprint(interface.get_messages("inventory.no_consumable_items"), width=63)
        return

def equipment_view(self):
    interface.print_title("equipment")
    interface.print_message(
        "equipment.list_line", 
        "left", 
        location="Location", 
        name="Name Item",
    )
    for location, equipment_item in self.equipment.items():
        if self.equipment["two_hand"] and location in ("main_hand", "off_hand") or location == "two_hand" and not equipment_item:
            continue
        interface.print_message(
            "equipment.list_line", 
            "left", 
            location=location.replace("_", " ").capitalize(), 
            name=equipment_item.name if equipment_item else "-",
        )


def player_view(self):
    interface.leftprint(self.name + " : ")
    WIDTH = 22
    DISTANCE = 5
    for name, stats in DATA["values"].items():
        lines = {}
        one_line = False
        for stat in stats:
            value = getattr(self, stat, None)
            if name == "critical" or stat == "armor_penetration":
                value = str(value) + "%"

            if name == "resource":
                one_line = True
                value = str(getattr(self, "max_" + stat)) + " / " +  str(getattr(self, stat))
            lines[util.short_stat(stat)] = value
        interface.generates_readable_stats(lines, use_sign=False, width=WIDTH, one_line=one_line, distance=DISTANCE)

    level = str(self.level)
    if self.level > self.max_level:
        level += "  (max)"

    interface.generates_readable_stats(
        {"level": level, "class": self._class}, 
        use_sign=False, width=WIDTH, one_line=True, distance=DISTANCE
    )

    exp = "|" + interface.progress_bar(self.exp, self.max_exp, width=25) + "|  "
    if self.level < self.max_level:
        exp += "{} / {} - {}%".format(self.exp, self.max_exp, int(100 / self.max_exp * self.exp))
    interface.leftprint("exp " + exp, distance=DISTANCE, width=len(exp) + 10)
    interface.printtwolines(f"Silver {self.silver}", f"{self.gold} Gold", width=WIDTH, distance=DISTANCE)


def attacks_view(self):
    interface.print_title("list of Attack")
    distance = 5
    for i, attack in enumerate(self.attacks):
        interface.leftprint("{:>2}) {}".format(i + 1, attack.name), distance=0)
        interface.leftprint(
            interface.get_messages("attack.cooldown").format(attack.cooldown),
            interface.get_messages("attack.mana_cost_template").format(attack.cost_mana),
            interface.get_messages("attack.stamina_cost_template").format(attack.cost_stamina),
            distance=distance
        )