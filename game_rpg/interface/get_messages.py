from ..setup import SETTING, LANG

def get_messages(index: str, default=None) -> str:
    return LANG()[SETTING["lang"]].get(
        index, LANG()["en_US"].get(
            index, index if not default else default
        )
    )