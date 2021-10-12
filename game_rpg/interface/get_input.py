from .. import setup
from .print_methode import print_
from .get_messages import get_messages


def get_input(add_text: str = ""):
    return input(
        add_text + setup.SETTING["input_prompt"]
    ).strip().lower()


def get_enter(text=""):
    input(
        text if text else get_messages("input_messages.get_enter")
    )
    print()
    return


def get_boolean_input(add_text: str = ""):
    while True:
        received_input = get_input(add_text)

        if received_input in get_messages("input_messages.forms_of_true"):
            return True

        if received_input in get_messages("input_messages.forms_of_false"):
            return False

        print()
        print_(get_messages("input_messages.get_boolean_input"))


def get_int_input(upper_limit):
    while True:
        _input = get_input()
        print()
        value = None

        try:
            value = int(_input)
        except ValueError:
            print_(get_messages("input_messages.get_int_input").format(upper_limit=upper_limit))
            # print()
            continue
            
        if not 1 <= value <= upper_limit:
            print_(get_messages("input_messages.get_int_input").format(upper_limit=upper_limit))
            # print()
            continue
        
        return value
            