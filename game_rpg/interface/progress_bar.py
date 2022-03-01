
def progress_bar(n: int, max_n: int, width: int=30, flip: bool = False):

    line = ""
    bar = int(width / max_n * n)

    while  bar > 0:
        line += "-"
        bar -= 1

    while len(line) < width:
        line += " "
        if len(line) == width:
            break

    if flip:
        line = line[::-1]

    return line
