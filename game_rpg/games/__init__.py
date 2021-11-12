from .camp import main as camp
from .main_menu import main as main_menu
from .adventure import main as adventure
from .shop import main as shop


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