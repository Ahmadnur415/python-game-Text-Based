from .. import interface, setup, namespace
from ..items import EQUIPPABLE, CONSUMABLE
from operator import attrgetter


def view_inventory_interface(player):
    while True:
        print()
        player.view_inventory()

        if not player.inventory:
            return namespace.BACK

        interface.leftprint(
            interface.get_messages("input_messages.choose_items_interface").format(
                name="Items",
                index="1" if len(player.inventory) == 1 else f"1 - {len(player.inventory)}"
            ) + " / (s) sort items", distance=0
        )
        index = interface.get_input()
        print()
        if index == "b":
            return namespace.BACK

        if index == "s":
            player.inventory.sort(key=attrgetter("name"), reverse=True)
            continue

        if index in [str(i) for i in range(1, len(player.inventory) + 1)]:
            index = int(index) - 1

            items = player.inventory[index]
            player.items_interface(items)


def items_interface(player, items):

    command = [namespace.USE_ITEMS if isinstance(items.attribute, CONSUMABLE) or isinstance(items.attribute, EQUIPPABLE) and not items.attribute.use else namespace.REMOVE_ITEMS]
    command.extend([namespace.SELL_ITEMS])
    print()
    items.view_stats()
    interface.centerprint("-")
    index = interface.get_command(command, True)
    print()

    if index in [namespace.USE_ITEMS, namespace.CONSUME_ITEMS]:

        if isinstance(items.attribute, CONSUMABLE):
            player.consume_items(items)
                
        if isinstance(items.attribute, EQUIPPABLE):
            player.equip_items(items)

        if items.amount < 1:
                return

        return player.items_interface(items)

    if index == namespace.REMOVE_ITEMS and isinstance(items.attribute, EQUIPPABLE):
        for locate_equip, items_equip in player.equipment.items():
            if items_equip == items:
                player.unequip_items(locate_equip)
                interface.centerprint(interface.get_messages("player.item_unequipped").format(items.name))
                break
        else:
            items.attribute.use = False
        
        return 


    if index == namespace.SELL_ITEMS:
        interface.centerprint(f"-- {namespace.SELL_ITEMS.capitalize()} --")

        amount_sell = 1
        price = int(items.price["value"] / 2)
        if isinstance(items.attribute, EQUIPPABLE):
            if items.attribute.use:
                
                interface.centerprint(interface.get_messages("items.cant_sell"))
                interface.get_enter()
                return player.items_interface(items)
        
        # jumlah yang dijual
        amount_sell = items.amount
        if items.amount > 1:
            print()
            interface.leftprint(interface.get_messages("items.on_sell").format(name=items.name, amount=items.amount))
            to_sell = interface.get_int_input(items.amount)
            amount_sell = to_sell

        # print hasil jual
        interface.leftprint(
            interface.get_messages(
                "items.sell"
            ).format(
                name=items.name,
                amount = amount_sell,
                price=price * amount_sell,
                type_=items.price["type"]
            )
        )
        # meyakinkan player
        result = interface.get_boolean_input()
        if not result:
            return player.items_interface(items)
        

        # print berhasil dijual
        print()
        interface.centerprint(
            interface.get_messages(
                "items.successfully_sold"
            ).format(
                name=items.name,
                amount = amount_sell,
                price=price * amount_sell,
                type_=items.price["type"]
            )
        )
        interface.get_enter()

        setattr( player, items.price["type"], getattr(player, items.price["type"]) + price * amount_sell)
        items.amount -= amount_sell
        if items.amount < 1:
            player.inventory.remove(items)
            return 
        return player.items_interface(items)


def use_items_consumable_interface(player, show_messages=True):
    while True:
        player.view_inventory(namespace.CONSUMABLE)

        if not player.consumable_items:
            break

        num = "1" if len(player.consumable_items) == 1 else f"1 - {len(player.consumable_items)}"

        interface.leftprint(
            interface.get_messages("input_messages.choose_items_interface").format(
                name="Items",
                index=num
            )
        )

        index = interface.get_input()
        print()

        if index == "b":
            return namespace.BACK

        if index in [str(i) for i in range(1, len(player.consumable_items) + 1)]:
            index = int(index) - 1
        else:
            interface.print_(
                interface.get_messages("input_messages.get_enter") + " " + num + " or B\n"
            )
            print()
            continue

        items_to_use = player.consumable_items[index]
        result = player.consume_items(items_to_use, show_messages)
        if result:
            return namespace.BACK

def view_stats_interface(player):
    while True:
        POINT_LEVEL = "point level" + ('(+)' if player.point_level > 0 else '')
        commands = [namespace.VIEW_ATTACK, POINT_LEVEL]

        interface.centerprint("-- STATS PLAYER --")
        player.view_stats()
        interface.centerprint("-")
        _input = interface.get_command(commands, True)
        print()
        if _input == namespace.VIEW_ATTACK:
            
            interface.centerprint("-- ATTACK PLAYER --")
            player.view_attack()
            interface.centerprint("-")
            interface.get_enter()
            print()
            continue
        
        if _input == POINT_LEVEL:
            print()
            player.point_level_interface()
            continue

        if _input == namespace.BACK:
            return namespace.BACK


def point_level_interface(player):
    lines = {}
    commands = []
    index_stats = ""

    interface.centerprint("-- Point Level --")
    for i, stats in enumerate(setup.DATA_ENTITY["entity_values"]["primary"]):
        commands.append(stats)
        lines[f"{i+1}) {interface.get_messages('view.' + stats, stats)}"] = getattr(player, stats)
    interface.printData(lines, distance=3)
    interface.leftprint(interface.get_messages("player.point_level") + " " + str(player.point_level))
    _input = interface.get_command(commands)
    print()
    if _input in commands:
        index_stats = _input
    
    if _input == namespace.BACK or index_stats == "":
        return namespace.BACK
    
    if player.level < 1:
        return namespace.BACK

    while player.level > 0:
        interface.leftprint(
            index_stats + " " + str(getattr(player, index_stats)),
            " " * 4 + interface.get_messages(
                f"desc.{index_stats}"
            ),
            interface.get_messages("player.index_point_level").format(
                amount=player.point_level,
                stats=index_stats
            ) + " / (b) Back"
        )
        amount_input = interface.get_input()
        print()

        if amount_input == namespace.BACK:
            return namespace.BACK
        
        try:
            amount_input = int(amount_input)
        except ValueError:
            continue

        if not 1 <= amount_input <= player.point_level:
            continue
        
        player.point_level -= amount_input
        setattr(player, index_stats, getattr(player, index_stats) + amount_input)
        return player.point_level_interface()
