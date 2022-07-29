import textwrap
from ..namespace import LEFT, CENTER, RIGHT, DEFAULT, char


def print_(*values, justify: str = "left", width: int = 50, distance = 0) -> None:
    lines = justify_string(*values, justify=justify, width=width, distance=distance)
    for line in lines:
        print(line)


def print_title(title: str, width: int = 50, pattern: str = "== {title} ==", distance: int = 0):
    pattern = pattern.split("\n")
    for text in pattern:
        print_(text.format(title, title=title), justify=CENTER, width=width, distance=distance)


def justify_string(*values, justify: str = "left", width: int = 50, distance = 0) -> list:
    lines = []
    f_text = format_text(justify, width)
    for value in values:
        warp = warp_text(str(value), width)
        for text in warp:
            lines.append(" " * distance + f_text.format(text))
    return lines


def format_text(justify: str, width: int) -> str:
    return "{:" + char[justify] + str(width) + "}"


def warp_text(text: str, width = 50) -> list:
    warp_string = textwrap.wrap(text, width=width)
    return warp_string


def printtwolines(left: str, rigth: str, distance: int = 1, width: int = 25, flip_rigth: bool = True, limit_rigth: bool = True):
    def fillist(l, n):
        l.extend(["" for _ in range(0, n)])

    line = " " * distance +  format_text(LEFT, width) + " " + format_text( (RIGHT if flip_rigth else LEFT) , width if limit_rigth else (len(rigth) + 1))
    left = textwrap.wrap(left, width=width , break_long_words=True, break_on_hyphens=True)
    rigth = textwrap.wrap(rigth, width=width if limit_rigth else (len(rigth) + 1) , break_long_words=True, break_on_hyphens=True)
    max_n = max(len(left), len(rigth))

    fillist(left, max_n-len(left))
    fillist(rigth, max_n-len(rigth))
    for i in range(0, max_n):
        print_( line.format(left[i], rigth[i]) )


def fillList(l: list, n: int):
    l.extend(["" for _ in range(0, n)])


def readable_stat(stat, value, width_stat = DEFAULT, width = 50, flip_right = True, colon: bool = True) -> list:
    if width_stat == DEFAULT:
        width_stat = len(str(stat)) + 3

    lines = []
    width_value = width - width_stat - (3 if colon else 0) - 1
    line = format_text(LEFT, width_stat) + "{colon}" + (format_text(LEFT if flip_right else RIGHT, width=width_value))
    stats = warp_text(stat, width_stat)
    values = warp_text(str(value), width_value)
    max_n = max(len(stats), len(values))

    fillList(stats, max_n-len(stats))
    fillList(values, max_n-len(values))
    for i in range(0, max_n):
        lines.append(
            line.format(stats[i], values[i], colon=":" if i == 0 and colon else " ")
        )

    return lines


def generate_readable_stats(stats: dict, width = 50, distance = 0, colon: bool = True):
    n = int(len(stats) / 2) + len(stats) % 2
    width = int(width / 2) - 2
    values = list(stats.items())

    for _ in range(0, n):            
        left = readable_stat(values[0][0], values[0][1], width=width, width_stat=10, colon=colon)
        rigth = []
        if len(values) > 1:
            rigth = readable_stat(values[1][0], values[1][1], width=width, width_stat=10, colon=colon)
            values.pop(1)

        max_row = len(max(left, rigth))
        values.pop()
        fillList(left, max_row - len(left))
        fillList(rigth, max_row - len(rigth))
        for a, b in zip(left, rigth):
            print_(a + " " * 4 + b, distance=distance)


def print_black(count: int = 2):
    for _ in range(0, count):
        print()
