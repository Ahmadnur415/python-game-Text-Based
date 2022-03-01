from .print_methods import printtwolines
from ..namespace import BACK
from ..util import short_stat


def generate_readable_list(lines: list, number: bool=False, make_line: bool=True) -> str | list:

    processed_list = []

    for i, name in enumerate(lines):
        name = name.capitalize()
        if number:
            i += 1
            if name == BACK:
                i = "b"
            processed_list.append(f"({i}){name}" if make_line else "{:>2}) {}".format(i, name))
        else:
            processed_list.append(name)

    if not make_line:
        return processed_list

    if len(processed_list) > 1:
        processed_list.append("and " + processed_list.pop())

    delimiter = " "

    if len(processed_list) > 2:
        delimiter = "," + delimiter

    return delimiter.join(processed_list)


def generates_readable_stats(stats: dict, distance: int = 5, width = 21, use_colon: bool = True,
    use_sign: bool = True, one_line: bool = False, use_prepix: bool = False):

    def make_line_stat(stat) -> str:
        name, value = stat

        line = "> " if use_sign else ""
        line += ("{:<10} : " if use_colon else "{} ").format(short_stat(name))

        if isinstance(value, (int, float)):
            line += ("{:+}" if use_prepix else "{}").format(value)
        else:
            line += str(value)

        return line.replace("_", " ")

    stats = list(stats.items())

    n = int(len(stats) / 2) + len(stats) % 2

    for _ in range(0, len(stats) if one_line else n):

        if not stats:
            break

        left = make_line_stat(stats[0])
        rigth = ""
        _width = width

        if len(stats) > 1 and not one_line:
            rigth = make_line_stat(stats[1])

            stats.pop(1)
        else:
            _width += len(str(stats[0][1])) + 2

        printtwolines(
            left, rigth, distance, _width, False, False
        )
        stats.pop(0)
