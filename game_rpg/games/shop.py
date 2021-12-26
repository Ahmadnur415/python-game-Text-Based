from ..import interface, setup, until
from ..items import get_items, Items as ITEMS
from .game import game as GAME
from operator import attrgetter
import random

B_MARKET = "black market"
BUY_ITEMS = "buy items"
COUNT_ITENS = "count items"
BACK = "back"
NEXT = "next"
GO_BACK = "go back"

def enter(self, game):
    commands = list(setup.DATA_ITEMS["items_by_type"].keys())
    commands.append(B_MARKET)
    commands.extend(self.commands.copy())
    
    while True:

        interface.centerprint(interface.get_messages("game.title"), "-- " + str(self.name.upper()) + " --")

        for i, room in enumerate(commands):
            interface.leftprint(f"({i + 1}) {str(room).capitalize().replace('_', ' ')}")

        index = interface.get_int_input(len(commands)) - 1
        index = commands[index]

        if index in setup.DATA_ITEMS["items_by_type"]:
            self.shop_items(game, index)

        if index == B_MARKET:
            self.black_market(game)

        if index in self.commands:
            return index


def shop_items(self, game, type_items):
    items_by_type = setup.DATA_ITEMS["items_by_type"][type_items]
    id_items_list = []
    class_list = []
    class_name = ""

    for name in items_by_type:
        name = name.split("/")[0].split(".")[0]
        if name not in class_list:
            class_list.append(name)
    # =======
    if len(class_list) > 1:
        command = class_list
        command.append(BACK)
        interface.centerprint(interface.get_messages("game.title"), "-- " + str(self.name.upper()) + " --")
        
        for i, name in enumerate(command):
            interface.leftprint(f"({i + 1}) {str(name).capitalize().replace('_', ' ')}")
        
        index = interface.get_int_input(len(command)) - 1

        if command[index] == BACK:
            return

        class_name = command[index] + "." + type_items

    if len(class_list) == 1:
        class_name = class_list[0] + "." + type_items

    for i in items_by_type:
        if class_name in i:
            id_items_list.append(i)
    # =======
    self.index_shop_item(game, id_items_list, type_items)
 

def index_shop_item(self, game, list_id_items: list[str], type_items: str):
    items = []
    rows_items = []
    size_shop = setup.SETTING["size_shop"]

    # get items
    for identify in list_id_items:
        item = get_items(identify)
        if getattr(item, "in_shop", True):
            items.append(item)

    # sort item by quality and name
    items.sort(key=attrgetter("quality", "name"))
    while items != []:
        rows_items.append(items[:size_shop])
        items = items[size_shop:]
    
    index = 0

    while True:
        commands = []
        
        if index < 0:
            index = 0
        if index > len(rows_items) - 1:
            index = len(rows_items) - 1

        interface.centerprint(interface.get_messages("game.title"), "-- " + str(self.name.upper()) + " --")

        for i, item in enumerate(rows_items[index]):
            commands.append(item)
            print_line_items(item, i)

        left = ""
        rigth = ""
        if index != 0 and index < len(rows_items):
            commands.append(GO_BACK)
            left = f"<-- Go back [{len(commands)}]"
        if index >= 0 and index != len(rows_items) - 1:
            commands.append(NEXT)
            rigth = f" [{len(commands)}] Next Items -->"

        if left or rigth:
            interface.LeftRigthPrint(left, rigth, 4)

        # index commands and items
        index_commands = interface.get_command(commands)

        print()
        if index_commands == GO_BACK:
            index -= 1
            continue

        if index_commands == NEXT:
            index += 1
            continue
        
        if index_commands == BACK:
            return self.shop_items(game, type_items)
        
        if isinstance(index_commands, ITEMS):
            self.dealing_items(game, index_commands)


def dealing_items(self, game, items):
    interface.centerprint("-- " + str(self.name.upper()) + " --")
    items.view_stats()
    interface.centerprint("-")

    interface.print_(
        interface.get_messages(
            "game.shop.buy_items"
        ).format(
            count=getattr(game.player, items.price["type"]),
            type_=items.price["type"],
            name=items.name,
            price=(str(items.price["value"] * items.amount)),   #(str(items.price["value"] * items.amount) + f" (1 / {items.price['value']} {items.price['type']})") if items.amount > 1 else str(items.price["value"])
            other="" if items.amount == 1 else f"(1/{items.price['value']} {items.price['type']})"
        )
    )

    result = interface.get_boolean_input()
    print()

    # false
    if not result:
        return result

    # true
    if getattr(game.player, items.price["type"]) >= items.price["value"] * items.amount:
        setattr(game.player, items.price["type"], getattr(game.player, items.price["type"]) - items.price["value"] * items.amount)
        
        game.player.append_inventory(items)

        interface.centerprint(interface.get_messages("game.shop.purchased").format(name=items.name, count=items.amount))
    else:
        interface.centerprint(interface.get_messages("game.shop.failed_purchased").format(type_=items.price["type"], name=items.name))
    
    print()
    interface.get_enter()
    return result


def _generate_items_bc(self, game):

    list_items = []
    max_items = 5 + int(game.player.luck / 100)
    for _ in range(max_items):
        items = get_items(random.choice(setup.DATA_ITEMS["id"]))
        
        while items.identify in list_items:
            items = get_items(random.choice(setup.DATA_ITEMS["id"]))
        
        list_items.append(items)

        if items.typeItems in ["food", "potion"]:
            items.amount = random.randint(-items.quality + 6, -9 / 5 * items.quality + 10 + int(game.player.luck / 100) )
        
        if items.price["type"] == "gold":
            change_type = until.resolve_random_condition([
                (False, until.clamp(75 - int(game.player.luck / 30), 50, 75)),
                (True, until.clamp(25 + int(game.player.luck / 30), 25, 50))
            ])

            if change_type:
                items.price["type"] = "silver"
                items.price["value"] *= 100

        items.price["discount"] = random.randint( -3 * items.quality + 20, -5 * items.quality + 30 + int(game.player.luck / 100) )
        items.price["value"] -= int(items.price["value"] / 100 * items.price["discount"])
        self.items_bc.append(items)


def black_market(self, game):

    if not self.items_bc or len(self.items_bc) < 1:
        _generate_items_bc(self, game)

    while True:
        interface.centerprint(interface.get_messages("game.title"), "-- Black Market --")

        for i, item in enumerate(self.items_bc):
            print_line_items(item, i)

        # interface.centerprint("-")
        interface.leftprint(
            interface.get_messages(
                "input_messages.choose_items_interface"
            ).format(
                name="Items", index="1" if len(self.items_bc) == 1 else f"1 - {len(self.items_bc)}"
            ) + " / (r) Refresh for 3 Gold"
        )
        _input = interface.get_input()
        print()
        if _input == "r":
            if game.player.gold >= 3:
                game.player.gold -= 3
                self.items_bc.clear()
                _generate_items_bc(self, game)
            else:
                interface.centerprint(interface.get_messages("player.not_have_money").format("gold"))
                interface.get_enter()
            print()
            continue
        
        if _input == "b":
            return
        
        if _input in [str(i) for i in range(len(self.items_bc)+1)]:
            items = self.items_bc[int(_input)-1]
            buy_items = self.dealing_items(game, items)
            if buy_items:
                self.items_bc.remove(items)
                continue
        
        print()

def print_line_items(item, i=0):
    interface.leftprint(f"{i+1:<3}{item.name} " + (str(item.amount) + "x" if item.amount > 1 else ""))
    interface.LeftRigthPrint(f"quality : {item.get_quality}", f"{item.price['value'] * item.amount} {item.price['type']}", 4)


main = GAME(
    name="shop",
    enter=enter,
    commands=None,
    items_bc=[]
)
setattr(main, "shop_items", shop_items.__get__(main, main.__class__))
setattr(main, "dealing_items", dealing_items.__get__(main, main.__class__))
setattr(main, "black_market", black_market.__get__(main, main.__class__))
setattr(main, "index_shop_item", index_shop_item.__get__(main, main.__class__))