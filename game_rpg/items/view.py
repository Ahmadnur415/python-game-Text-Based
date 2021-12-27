from .. import interface, setup, namespace


def view_stats(items):
    interface.centerprint(" === " + items.name + " === ")
    base_stats = {
        "quality": items.get_quality,
        "type": items.typeItems.capitalize()
    }

    if items.namespace == namespace.EQUIPPABLE:
        interface.printData(base_stats, distance=1)
        view_EQUIPPABLE(items)

    if items.namespace == namespace.CONSUMABLE:
        base_stats.update({"amount": items.amount})
        interface.printData(base_stats, distance=1)
        view_CONSUMABLE(items)


def view_EQUIPPABLE(items):
    distance = 1

    if items.typeItems == 'weapons':
        damage_items = getattr(items.attribute, "damage", [0, 0])
        DMG = (" ~ ".join([str(i) for i in damage_items]) if isinstance(damage_items, list) else str(damage_items)) + " Damage"
        APEN = str(getattr(items.attribute, "armor_penetration", 0)) + "% armor penetration "
        interface.leftprint("Weapons Attribute (" + DMG + ", " + APEN + ")", distance=distance)

    for name in setup.DATA_ITEMS["attribute"]["basic"]:
        if name not in ("damage", "armor_penetration"):
            value = getattr(items.attribute, name, 0)
            
            if value != 0:
                interface.printData(
                    {interface.get_messages("view." + name, name): f"{value:+}"}, 
                    one_line=True, 
                    mark=False, 
                    distance=distance
                )

    for names, value in items.stats.items():
        interface.printData(
            {interface.get_messages("view." + names, names): f"{value:+}"},
            one_line=True, 
            mark=False, 
            distance=distance
        )


def view_CONSUMABLE(items):
    
    if items.attribute.type_ == "restore":
        lines = [] 
        for names, values in items.attribute.stats.items():
            if isinstance(values, dict):
                lines.append(names + f" from {values['value']}% {interface.get_messages('view.modiefer', 'modiefer')}")
            
            if isinstance(values, int):
                lines.append(f"{values} {names}")
        
        interface.centerprint(
            interface.get_messages(
                "desc.restore_items"
            ).format(
                interface.generate_readable_list(
                    lines
                )
            ), distance=1
        )
    
    if items.attribute.type_ == "increase":
        interface.leftprint(interface.get_messages("desc.increase_items"))
        for name, value in items.attribute.stats.items():
            
            if name in setup.DATA_ENTITY["entity_values"]["resource"]:
                name = "max_" + name

            interface.leftprint(f"{value} {interface.get_messages('view.' + name, name)}")