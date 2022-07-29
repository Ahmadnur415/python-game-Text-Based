import textwrap
from ..namespace import *


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

def fillList(l: list, n: int):
    l.extend(["" for _ in range(0, n)])

def print_(*values, justify: str = "left", width: int = 50, distance = 0)->None:
    lines = justify_string(*values, justify=justify, width=width, distance=distance)

    for line in lines:
        print(line)

def print_title(title: str, width: int=50, pattern: str="== {title} ==", distance=0):
    pattern = pattern.split("\n")
    for text in pattern:
        print_(text.format(title, title=title), justify=CENTER, width=width, distance=distance)
