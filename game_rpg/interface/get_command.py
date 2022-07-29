from typing import Union, Tuple, List
from .get_input import get_input
from .get_messages import get_messages
from ..namespace import BACK
from .print_methods import centerprint, leftprint, print_
from .generate_readable_data import generate_readable_list


def get_command(
    commands: List[str], 
    name_command: str = "", 
    list_option: bool = False,
    add_command_back: bool = True, 
    loop: bool = True
) -> Union[Tuple, bool]:

    while True:
        if not commands:
            return BACK

        if list_option:
            lines = commands.copy()
            if add_command_back:
                lines.append(BACK)

            leftprint(*generate_readable_list(lines, number=True, make_line=False), distance=1)

        len_command = len(commands)
        index = f"1 - {len_command}" if len_command > 1 else "1"
        if add_command_back:
            index += " or (b) Back"

        line = get_messages("input_messages.choose_items_interface").format(name=name_command, index=index) + " "
        if add_command_back:
            leftprint( line , distance=1 )
            line = ""

        received_input = get_input( line, distance=1 )
        if received_input.lower() == "b" and add_command_back:
            return (BACK, "b")

        if received_input in [str(i) for i in range(1, len_command + 1)]:
            return (commands[int(received_input) - 1], int(received_input))

        print_("\n")
        centerprint(
            get_messages(
                "input_messages.get_enter"
            ) + " " + index
        )
        print_("\n")
        if not loop:
            return False
