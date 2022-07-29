from ..data import _load


def get_messages(index: str, default = None) -> str:
    LANG = _load("lang.json")
    return LANG.get(index, default)
