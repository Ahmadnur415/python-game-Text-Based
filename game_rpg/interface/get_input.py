from typing import Union, Optional
from .get_messages import get_messages
from .print_methods import leftprint, centerprint, print_


def get_input(add_text: Optional[str] = None, distance: int = 0):
    if not add_text:
        add_text = ""

    return input(
        " " * distance + \
        add_text +  get_messages("input_messages.input_prompt", ">>>") + " "
    ).strip().lower()


def get_enter(text: str = ""):
    centerprint(text if text else get_messages("input_messages.get_enter"))
    input()
    print_()
    return


def get_boolean_input():
    while True:
        received_input = get_input(distance=1)
        if received_input in get_messages("input_messages.forms_of_true", ["y", "yes"]):
            return True

        if received_input in get_messages("input_messages.forms_of_false", ["n", "no"]):
            return False

        print_()
        leftprint(get_messages("input_messages.get_boolean_input"))


def get_int_input(upper_limit, add_text: Optional[str] = None):
    while True:
        _input = get_input(add_text, 1)
        print_()
        value = None

        try:
            value = int(_input)
        except ValueError:
            leftprint(get_messages("input_messages.get_int_input").format(upper_limit=upper_limit))
            continue

        if not 1 <= value <= upper_limit:
            leftprint(get_messages("input_messages.get_int_input").format(upper_limit=upper_limit))
            continue

        return value
