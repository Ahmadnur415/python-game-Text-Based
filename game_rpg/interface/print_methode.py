import textwrap
from .. import setup


def printData(data: dict = None, one_line=False, mark=True, distance=8, **kwargs):
    if data is None:
        data = {}
    data.update(kwargs)
    lines_key, lines_values = [], []
    distance = (" " * distance) if isinstance(distance, int) else " "

    line_1 = "{}{mark} {}"
    line_2 = line_1 + " - {}{mark} {}"

    if mark:
        line_1 = "{:<9}{mark} {:<12}"
        line_2 = line_1 + "{:<9}{mark} {}"

    mark = ":" if mark else ""

    for name_key, value in data.items():
        name_key = name_key.replace("_", " ")
        if one_line or len(str(value)) >= 10:
            print(distance + line_1.format(name_key, value, mark=mark))
        else:
            lines_key.append(name_key)
            lines_values.append(value)
            if len(lines_key) == len(lines_values) == 2:
                print(distance + line_2.format(lines_key[0], lines_values[0], lines_key[1], lines_values[1], mark=mark))
                lines_key.clear()
                lines_values.clear()

    if len(lines_key) == len(lines_values) == 1:
        # print(k, v)
        print(distance + line_1.format(lines_key[0], lines_values[0], mark=mark))


def list_line(line: list, number: bool = False, pemisah: str = ",", replace: tuple = None, andTxt: bool = True):
    text = ""
    end = ""
    pemisah = " " + pemisah + " "
    if len(line) == 2 and andTxt:
        pemisah = " "

    for i, txt in enumerate(line):

        if replace and len(replace) == 2 and isinstance(txt, str):
            txt = txt.replace(replace[0], replace[1]).capitalize()

        if (i + 1) == len(line):
            end = "" if not andTxt else "and "
            pemisah = ""
        if number:
            txt = f"[{i + 1}]" + txt
        text += f"{end}{txt}{pemisah}"

    return text


def generate_readable_list(lines: list, number=False):
    processed_list = [
        "{num}{names}".format(num="" if not number else f"({i + 1})", names=names) for i, names in enumerate(lines)
    ]

    if len(processed_list) > 1:
        processed_list.append("or " + processed_list.pop())

    delimiter = " "

    if len(processed_list) > 2:
        delimiter = "," + delimiter

    return delimiter.join(processed_list)


def dict_line(data: dict, short_text: bool = True, **kwargs):
    line = ""
    data.update(kwargs)
    koma = ","
    for i, key in enumerate(data):
        if (i + 1) == len(data) and len(data) > 1:
            line += "and "
            koma = ""
        value = data[key]

        if key in setup.GAME["_view"] and short_text:
            key = setup.GAME["_view"][key]

        line += f"{key} {value}{koma} "
    return line


def print_(*text):
    for txt in text:
        WrapString = textwrap.wrap(txt, width=50)
        for line in WrapString:
            print(line)


def centerprint(*text, distance=0):
    f_txt = (" " * distance) + "{:^" + str(50 - (distance * 2)) + "}" + (" " * distance)
    for txt in text:
        if txt == "":
            print()
            continue

        WrapString = textwrap.wrap(txt, width=50 - distance)
        for line in WrapString:
            print(f_txt.format(line))


def leftprint(*text: str, distance: int = 1):
    f_txt = (" " * distance) + "{}"
    for txt in text:
        WrapString = textwrap.wrap(str(txt), width=50 - distance)
        for line in WrapString:
            print(f_txt.format(line))


def LeftRigthPrint(left: str, right: str, distance: int = 1):
    d = " " * distance
    start = d + left
    mid = "{:>" + str(50 - len(start) - len(d)) + "}" + d
    end = mid.format(right)

    print(start + end)

if __name__ == '__main__':
    printData()
