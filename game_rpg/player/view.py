from .. import interface, setup


def view_equipment(player):
    DATA = setup.DATA_ENTITY.copy()

    lines = ["== Equipment ==".center(50)]
    if not player.equipment["two_hand"]:
        lines += [
            f"{locations.replace('_', ' ').capitalize():<15} : {'-' if not player.equipment[locations] else player.equipment[locations].name}"
            for locations in ["main_hand", "off_hand"]
        ]

    if player.equipment["two_hand"]:
        lines += [f"{'Two Hand':<15} : {player.equipment['two_hand'].name}"]

    lines += [
        f"{location.replace('_', ' ').capitalize():<15} : {'-' if not player.equipment[location] else player.equipment[location].name}"
        for location in DATA['attribute']["equipment"]["armor"]
    ]

    for line in lines:
        print(" " + line)


def view_stats(self):
    lines = {}
    distance = 3

    for stats in setup.DATA_ENTITY["stats"]:
        line = str(getattr(self, stats, 0))
        if stats in setup.DATA_ENTITY["entity_values"]["resource"]:
            line = str(getattr(self, stats, 0)) + " / " + str(getattr(self, "max_" + stats, 0))

        lines.update({interface.get_messages("view."+stats, stats): line})

    lines.update({
        interface.get_messages("view.critical_change", "C.Change"): str(self.critical_change) + "%",
        interface.get_messages("view.critical_hit", "C.Hit"): self.critical_hit  + "%",
        "Level": self.level
    })
    if self.namespace == "player":
        _exp = getattr(self, "exp", 0)
        _max_exp = getattr(self, "max_exp", 0)
        line = "0 / 0 | 0% (max)"
        if self.level < 60:
            line = str(_exp) + " / " + str(_max_exp) + " | " + str(round((100 * _exp) / _max_exp, 2)) + "%"

        lines.update({"Exp": line, "Gold": getattr(self, "gold", 0), "Silver": getattr(self, "silver", 0)})

    print(f"{self.name} Stats: ")
    interface.printData(
        lines, distance=distance
    )


def view_inventory(player, typeItems: str = None):
    title = "Inventory"

    if not player.inventory:
        interface.centerprint(interface.get_messages("inventory.no_have_items"))
        return

    if typeItems in ("EQUIPPABLE", "equippable") and not player.equippable_items:
        interface.centerprint(interface.get_messages("inventory.no_equippable_items"))
        return

    if typeItems in ("CONSUMABLE", "consumable") and not player.consumable_items:
        interface.centerprint(interface.get_messages("inventory.no_consumable_items"))
        return

    interface.centerprint("== " + (title if not typeItems else typeItems) + " ==")

    items_to_show = []
    for items in player.inventory:
        if not typeItems or typeItems.upper() == items.namespace:
            items_to_show.append(items)

    interface.leftprint(f"{'NO':<3}{'Name'}")

    for index, inventory_items in enumerate(items_to_show):
        name = inventory_items.name
        if inventory_items.amount > 1:
            name += f" {inventory_items.amount}x"

        if inventory_items.namespace == "EQUIPPABLE":
            name += (" - [E]" if inventory_items.attribute.use else "")

        interface.leftprint(f"{index + 1:<3}{name}")
        interface.LeftRigthPrint(f"Quality : {inventory_items.get_quality.capitalize()}", inventory_items.typeItems.capitalize(), 4)


def use_items_interface(player):
    while True:
        player.view_inventory("CONSUMABLE")

        if not player.consumable_items:
            break
