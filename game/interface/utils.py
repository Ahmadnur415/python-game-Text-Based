from ..game import console


def clear(*, f: bool = False):
    if f:
        [print() for _ in range(200)]
    console.clear()
