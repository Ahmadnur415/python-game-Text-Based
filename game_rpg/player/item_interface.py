from .. import interface, namespace


def item_interface(player, item):
    while True:

        commands = [namespace.USE_ITEMS, namespace.SELL_ITEMS]
        if item.used and item.class_item == namespace.EQUIPPABLE:
            commands[0] = namespace.REMOVE_ITEMS

        if item.class_item == namespace.CONSUMABLE:
            commands[0] = namespace.CONSUME_ITEMS

        item.view()
        interface.print_message(
            "item.desc.price", "left", price=item.selling_price[0], name=item.selling_price[1]
        )

        interface.centerprint("-")

        command = interface.get_command(commands, loop=False, list_option=True)

        if not isinstance(command, tuple):
            continue

        interface.print_("\n")

        index = command[0]

        if index == namespace.REMOVE_ITEMS and item.used:
            player.unequip_item(item.location_used)

        if index == namespace.USE_ITEMS:
            player.equip_items_interface(item)

        if index == namespace.SELL_ITEMS:
            player.sell_item(item)

            if item.amount < 1:
                return

        if index == namespace.CONSUME_ITEMS:

            player.consume_item(item)
            interface.print_("\n")

            if item.amount < 1:
                return


        if index == namespace.BACK:
            return index

def sell_item(player, item):

    if item.used:
        interface.centerprint(interface.get_messages("item.cant_sell"))
        interface.get_enter()
        interface.print_("")
        return

    amount_to_sell = 1
    if item.amount > 1:
        interface.print_message("item.on_sell", amount=item.amount, name=item.name )
        amount_to_sell = interface.get_int_input(item.amount, interface.get_messages("input_messages.choose").format(item.amount))

    price = item.selling_price[0] * amount_to_sell

    interface.print_message(
        "item.sell", "left", amount = amount_to_sell, name = item.name, price = price, type_ = item.selling_price[1]
    )


    result = interface.get_boolean_input()
    if not result:
        return result

    interface.print_("\n")
    interface.print_message(
        "item.successfully_sold", amount = amount_to_sell, name = item.name, price = price, type_ = item.selling_price[1]
    )
    interface.get_enter()

    setattr( player, item.selling_price[1], getattr(player, item.selling_price[1]) + price)
    item.amount -= amount_to_sell
    if item.amount < 1:
        player.remove_items(item)

    return
