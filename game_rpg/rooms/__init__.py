from .camp import ROOM as camp
from .main_menu import ROOM as main_menu
from .adventure import ROOM as adventure
from .shop import ROOM as shop


main_menu.add_commands(
    adventure.name,
    shop.name,
    camp.name
)

camp.add_commands(
    main_menu.name
)

shop.add_commands(
    main_menu.name
)