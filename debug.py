from typing import NewType

STR = NewType('STR', str)

def func()-> STR:
    return str(1)
