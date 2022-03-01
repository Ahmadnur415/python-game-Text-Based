from .print_methods import format_text
from .get_messages import get_messages
from ..item import Item
from .. import namespace
import textwrap


def readable_item(item, lines: tuple):
    width = get_messages("item.width")
    line = ""

    if not isinstance(lines, tuple):
        return

    for name in lines:
        if name not in width:
            continue

        value = getattr(item, name, name)
        if isinstance(value, list):
            value = " ".join([str(i) for i in value])

        value = value.capitalize()

        if isinstance(item, Item) and name.lower() == "name":
            value = textwrap.shorten(value, width[name])

            if item.class_item == namespace.EQUIPPABLE and item.used:
                value += " [E]"

            if item.class_item == namespace.CONSUMABLE and item.amount > 1:
                value += " " + str(item.amount) + "x"

        line += " | " + format_text("<", width[name]).format(value)

    return line
