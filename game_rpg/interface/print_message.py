from .print_methods import leftprint, centerprint
from .get_messages import get_messages


def print_message(message, position:str = "center", *args, **kwargs):
    print_ = centerprint
    if position == "left":
        print_ = leftprint

    print_( get_messages(message).format(*args, **kwargs) )
