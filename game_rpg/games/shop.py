from ..import interface, setup, until, file
from ..items import get_items, Items as ITEMS
from .game_menu import game_menu
from operator import attrgetter
import random

B_MARKET = "black market"
BUY_ITEMS = "buy items"
COUNT_ITENS = "count items"
BACK = "back"
NEXT = "next"
GO_BACK = "go back"

def enter(self, game):
    
    setup.DATA_ITEMS = file._load_items(setup.GAME["fileGame"]["items"])
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
    id_items = {}           # example {"long_sword": ["long_sword:wooden", "class_id:items_id"]}
    class_id_name = ""
    list_id_items = []      # list of class_id_items
    items = []              # all_of_items
    max_rows_items = 8
    row_items = []          # array untuk items // 1 array / max_rows_items

    # filter id items
    for name in setup.DATA_ITEMS["items_by_type"][type_items]:
        class_name = name.split(":")[0]

        if not id_items.get(class_name):
            id_items[class_name] = []
        id_items[class_name].append(name)

    # interface shop 1 jika jumlah id items lebih dari 1
    if len(id_items) > 1:
        command = list(id_items.keys())
        command.append(BACK)
        interface.centerprint(interface.get_messages("game.title"), "-- " + str(self.name.upper()) + " --")
        
        for i, name in enumerate(command):
            interface.leftprint(f"({i + 1}) {str(name).capitalize().replace('_', ' ')}")
        
        index = interface.get_int_input(len(command)) - 1
        class_id_name = command[index]
        
        # back commands
        if class_id_name == BACK:
            return
        # index
        list_id_items = id_items.get(class_id_name)

    # jika terdapat 1 id_class
    if len(id_items) == 1:
        class_id_name = list(id_items.keys())[0]
        list_id_items = id_items[class_id_name]

    # make new line
    print()

    # load items // di load biar bisa di urutkan bedasarkan quality
    for name in list_id_items:
        item = get_items(name)
        if getattr(item, "in_shop", True):
            items.append(item)        

    # sort items
    items.sort(key=attrgetter("quality", "name"))

    # dibagi 10 / 1 
    rows = []
    for item in items:
        rows.append(item)
        if len(rows) == max_rows_items:
            row_items.append(rows.copy())
            rows.clear()
    if rows:
        row_items.append(rows.copy())
        rows.clear()

    # interface shop 2
    index_row = 0           # index_row
    while True:
        items_in_shop = []  # items yang yang ingin di tampilkan
        commands = []

        if index_row < 0:
            index_row = 0
        if index_row > len(row_items) - 1:
            index_row = len(row_items) - 1

        # print title
        interface.centerprint(interface.get_messages("game.title"), "-- " + str(self.name.upper()) + " --")

        # menambahkan items untuk di tampilkan
        if len(items) <= 10 and len(row_items) == 1:
            items_in_shop.extend(items)
        
        if len(items) > 10 and len(row_items) > 1:
            items_in_shop.extend(row_items[index_row])

        # print items
        for i, show_items in enumerate(items_in_shop):
            commands.append(show_items)
            interface.leftprint(f"{i+1:<3}{show_items.name}")
            interface.LeftRigthPrint(f"quality : {show_items.get_quality.capitalize()}", f"price : {show_items.price['value']} {show_items.price['type']}", 4)    

        # menambahkan commands dan print
        left = ""
        rigth = ""
        if index_row != 0 and index_row <= len(row_items) - 1:
            commands.append(GO_BACK)
            left = f"<-- Go back ({len(commands)})"
        if index_row >= 0 and index_row != len(row_items) - 1:
            commands.append(NEXT)
            rigth = f" ({len(commands)}) Next Items -->"

        if left or rigth:
            interface.LeftRigthPrint(left, rigth, 4)
        

        # index commands and items
        index_commands = interface.get_command(commands)

        print()
        if index_commands == GO_BACK:
            index_row -= 1
            continue

        if index_commands == NEXT:
            index_row += 1
            continue
        
        if index_commands == BACK:
            return
        
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

    id_items = []

    for _ in range(5 + int(game.player.luck / 100)):
        item = random.choice(setup.DATA_ITEMS["all_items"])
        items = get_items(item)
        
        while item in id_items:
            item = random.choice(setup.DATA_ITEMS["all_items"])
            items = get_items(item)
        
        id_items.append(item)

        if items.typeItems in ["food", "potion"]:
            items.amount = random.randrange(5 + int(game.player.luck / 100))
        
        if items.price["type"] == "gold":
            chnage_type = until.resolve_random_condition([
                (False, until.clamp(75 - int(game.player.luck / 30), 50, 75)),
                (True, until.clamp(25 + int(game.player.luck / 30), 25, 50))
            ])

            if chnage_type:
                items.price["type"] = "silver"
                items.price["value"] *= 100

        items.price["discount"] = random.randrange(items.price["max_discount"] + int(game.player.luck / 50))
        items.price["value"] -= int(items.price["value"] / 100 * items.price["discount"])
        self.items_bc.append(items)


def black_market(self, game):

    if not self.items_bc or len(self.items_bc) < 2:
        _generate_items_bc(self, game)

    while True:
        interface.centerprint(interface.get_messages("game.title"), "-- Black Market --")

        for i, item in enumerate(self.items_bc):
            interface.leftprint(f"{i+1:<3}{item.name} " + (str(item.amount) + "x" if item.amount > 1 else ""))
            interface.LeftRigthPrint(f"quality : {item.quality}", f"price : {item.price['value'] * item.amount} {item.price['type']}", 4)

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

main = game_menu(
    name="shop",
    enter=enter,
    commands=None,
    items_bc=[]
)
setattr(main, "shop_items", shop_items.__get__(main, main.__class__))
setattr(main, "dealing_items", dealing_items.__get__(main, main.__class__))
setattr(main, "black_market", black_market.__get__(main, main.__class__))