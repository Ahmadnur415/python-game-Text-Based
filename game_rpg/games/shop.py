from .game import Game
from ..items import DATA
from .. import interface, namespace, util
from ..item import get_items

def enter(self, player):

    self.index_row = 0
    sort_by = [namespace.NAME, namespace.PRICE, namespace.QUALITY]

    while True:
        interface.print_title( self.name.capitalize() )
        result = interface.get_command(list(DATA[self.index].keys()), "type of items", list_option=True, loop=False)

        if not isinstance(result, tuple):
            continue

        if result[0] == namespace.BACK:

            interface.print_("\n")
            from .main import main as main_menu
            return main_menu.enter(player)

        break


    self.typeitem = result[0]

    interface.print_("\n")
    while True:
        rows = getattr(self, "get_item_by_" + self.sort_by)()
        interface.print_title(self.name.capitalize() + " " + self.typeitem, )

        sort_by = [namespace.NAME, namespace.PRICE, namespace.QUALITY]
        sort_by.remove(self.sort_by)

        LEFT = ""
        RIGTH = ""

        if self.index_row < 0:
            self.index_row = 0

        if self.index_row > len(rows) - 1:
            self.index_row = len(rows) - 1

        items = [
            get_items(name) for name in rows[self.index_row]
        ]

        self.print_line("No", "")

        for i, item in enumerate(items):
            self.print_line(i + 1, item)

        interface.leftprint(
            interface.get_messages("game.shop.sort_item").capitalize(),
            *(" " * 4 + interface.get_messages("game.shop.sort_item_line").format(len(items) + i + 1, name) for i , name in enumerate(sort_by))
        )

        items.extend(sort_by)

        if self.index_row > 0 and self.index_row < len(rows):
            LEFT = interface.get_messages("game.shop.go_back").format(len(items) + 1)
            items.append(LEFT)

        if self.index_row > -1 and self.index_row < len(rows) - 1:
            RIGTH = interface.get_messages("game.shop.next").format(len(items) + 1)
            items.append(RIGTH)

        interface.printtwolines(LEFT, RIGTH)
        interface.print_message("game.shop.player_coin", "left", silver = player.silver, gold = player.gold )

        result = interface.get_command(items, "to buy", loop=False)

        if not isinstance(result, tuple):
            continue

        interface.print_("\n")

        if result[0] == LEFT:

            self.index_row -= 1
            continue

        if result[0] == RIGTH:

            self.index_row += 1
            continue

        if result[0] in sort_by:
            self.sort_by = result[0]
            self.index_row = 0
            continue

        if result[0] == namespace.BACK:
            return self.enter(player)

        item = result[0]

        if getattr(player, item.price[1]) < item.price[0]:

            interface.print_message("game.shop.failed_purchased", type_ = item.price[1], name = item.name )
            interface.get_enter()
            continue

        item.view()

        interface.centerprint("-")
        interface.print_message(
            "game.shop.buy_item", "left", value = getattr(player, item.price[1]), type_ = item.price[1], name = item.name, price = item.price[0] * 1, other = ""
        )

        result = interface.get_boolean_input()
        interface.print_("\n")

        if not result:
            continue

        setattr(player, item.price[1], getattr(player, item.price[1]) - item.price[0])
        player.add_items(item)

        interface.print_message("game.shop.purchased", name=item.name, count=item.amount)

        interface.get_enter()
        interface.print_("")


def print_line(_, i, item):
    interface.leftprint(
        interface.get_messages("item.line_item").format(
            i , interface.readable_item(item, ("name", "type", "quality", "price"))
        ),
        width=100
    )


def sort_items(self, key: str) -> list:
    # sorting item
    data = [
        item[0] for item in sorted(
            [
                (id_item , DATA["items"][id_item]) for id_item in DATA[self.index][self.typeitem]
            ],
            key=lambda d : d[1][key]
        )
    ]

    return util.generate_rows_list(self.count_item, data)


def get_item_by_price(self):
    items_price_silver = []
    items_price_gold = []

    for identify in DATA[self.index][self.typeitem]:
        item = DATA["items"][identify].copy()

        if item["price"][1] == "gold":
            items_price_gold.append((identify, item))
            continue

        items_price_silver.append((identify, item))

    items = sorted(items_price_silver, key=lambda d : d[1]["price"][0]) + sorted(items_price_gold, key=lambda d : d[1]["price"][0])

    return util.generate_rows_list(self.count_item, [item[0] for item in items])


def get_item_by_quality(self):
    return self.sort_items("quality")


def get_item_by_name(self):
    return self.sort_items("name")


def make_row_items(self, items):
    rows_items = []

    while data != []:
        rows_items.append(items[:self.count_item])
        data = data[self.count_item:]

    return rows_items


main = Game(
    namespace.SHOP,
    enter,
    index="items_by_namspace",
    index_row=0,
    count_item=8,
    typeitem="",
    sort_by=namespace.QUALITY
)

main.add_methode("print_line", print_line)
main.add_methode("sort_items", sort_items)
main.add_methode("get_item_by_price", get_item_by_price)
main.add_methode("get_item_by_quality", get_item_by_quality)
main.add_methode("get_item_by_name", get_item_by_name)
