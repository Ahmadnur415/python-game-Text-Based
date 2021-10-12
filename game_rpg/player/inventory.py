from ..items import EQUIPPABLE, CONSUMABLE


def append_inventory(player, *item):
    for items in item:
        if not items:
            continue
        if not player.inventory or isinstance(items.attribute, EQUIPPABLE):
            player.inventory.append(items)
        elif isinstance(items.attribute, CONSUMABLE):
            for inventory_items in player.inventory:
                # items bila ada yang sama
                if inventory_items.typeItems == items.typeItems and inventory_items.identify == items.identify:
                    inventory_items.amount += items.amount
                    break
            else:
                player.inventory.append(items)


def remove_items(player, *items):
    for item in items:
        if item in player.inventory:
            player.inventory.remove(item)

    # generate
    for item in player.inventory:
        if item.amount < 1:
            player.inventory.remove(item)


@property
def equippable_items(player):
    items = []
    for item in player.inventory:
        if isinstance(item.attribute, EQUIPPABLE):
            items.append(item)

    return items


@property
def consumable_items(player):
    items = []
    for item in player.inventory:
        if isinstance(item.attribute, CONSUMABLE):
            items.append(item)

    return items
