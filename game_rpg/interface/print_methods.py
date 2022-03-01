import textwrap
from .get_messages import get_messages

print_ = print


def print_warp(*values, ftxt: str, width: int):
    for value in values:
        WrapString = textwrap.wrap(str(value), width=width)
        for line in WrapString:
            print_(ftxt.format(line))


def centerprint(*values, distance: int = 0, width: int = 50):
    line = " " * distance + format_text("^", width)

    return print_warp(*values, ftxt=line, width=width)


def leftprint(*values, distance: int =  1, width: int = 50):
    return print_warp(*values, ftxt=" " * distance + "{}", width=width - distance)


def printtwolines(left: str, rigth: str, distance: int = 1, width: int = 25, flip_rigth: bool = True, limit_rigth: bool=True):

    def fillist(l, n):
        l.extend(["" for _ in range(0, n)])

    line = " " * distance +  format_text("<", width) + " " + format_text( (">" if flip_rigth else "<") , width if limit_rigth else (len(rigth) + 1))

    left = textwrap.wrap(left, width=width , break_long_words=True, break_on_hyphens=True)
    rigth = textwrap.wrap(rigth, width=width if limit_rigth else (len(rigth) + 1) , break_long_words=True, break_on_hyphens=True)

    max_n = max(len(left), len(rigth))

    fillist(left, max_n-len(left))
    fillist(rigth, max_n-len(rigth))

    for i in range(0, max_n):
        print_( line.format(left[i], rigth[i]) )


def print_title(title: str, width: int = 50):
    text = get_messages("game.title." + title)

    if not text:
        text = get_messages("game.title.template").format(title.capitalize())

    centerprint( text, width=width )

def format_text(pos: str, width: int) -> str:
    return "{:" + pos + str(width) + "}"
