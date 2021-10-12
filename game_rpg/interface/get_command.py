from .print_methode import centerprint, print_, generate_readable_list
from .get_input import get_input
from .get_messages import get_messages


def get_command(command: list, list_option = False):
    # command.append("back")
    while True:
        
        if not command:
            return "back"

        if list_option:
            centerprint(generate_readable_list(command, True) + " / (b) Back", "-", distance=0)
        index = "1" if len(command) == 1 else f"1 - {len(command)}"
        
        print_(get_messages("input_messages.choose_items_interface").format(name="", index=index))
        
        # print()

        received_input = get_input()
        if received_input.lower() == "b":
            return "back"
        
        if received_input in [str(i) for i in range(1, len(command) + 1)]:
            return command[int(received_input) - 1]
        
        print("")
        centerprint(
            get_messages(
                "input_messages.get_enter"
            ) + " " + index  + " or b (back)"
        )
        print()
