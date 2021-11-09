import os
import json
from game_rpg.file import item, lang


def _load(filename):
    data = json.load(
        open(
            os.path.dirname(
                os.path.realpath(__file__)
            ) + "\\" + filename
        )
    )
    return data


def _init():
    core = _load("game.data.json")
    for name, path in core["fileGame"].items():
        data = None
        if name == "items":
            data = _load_items(path)
        elif name == "lang":
            data = _load_lang(path)
        elif name == "entity":
            data = _entity_data(path)
        else:
            data = _load(path)

        core[name] = data

    return core

# version 3
def _load_items(path: str):
    items = _load(path)

    if not items.get("items"):
        items["items"] = {}

    all_items = []
    items_by_type = {}

    for items_path in item.items:
        # load
        try:
            data_class = _load(items["path"] + items_path)
        except (FileNotFoundError) as e:
            print(e.args[1], f": .\\{items_path}")
            continue

        data_class['name'] = data_class['name'].lower().replace(" ", "_")

        if not items["items"].get(data_class["name"]):
            items["items"][data_class['name']] = data_class
        else:
            continue


        for name_items, data_items in data_class["items"].items():
            # print(name_items, "||", data_items)
            identify = data_class['name'] + ":" + name_items
            data_items["identify"] = identify

            # menambahkan identify ke all items dan ke items by type
            all_items.append(identify)
            if not items_by_type.get(data_class["type_items"]):
                items_by_type[data_class["type_items"]] = []
            items_by_type[data_class["type_items"]].append(identify)

            # set type items || example : weapons, armor, potion, food
            data_items["type_items"] = data_class["type_items"]

            # set data items untuk class
            if data_class["class"] == "EQUIPPABLE":
                if data_class["type_items"] == "weapons":
                    # get style attack dari data class
                    data_items["styleAttack"] = data_class["styleAttack"]
                # get location, user, classItems to equip items dari data class
                data_items["location"] = data_class["location"] if not data_items.get("location", None) else data_items[
                    "location"]
                data_items["user"] = data_class['user'] if not data_items.get("user", None) else data_items["user"]
                data_items["classItems"] = data_class["name"]  # example : axe, armor, wand, helmet

    items['all_items'] = all_items
    items["items_by_type"] = items_by_type
    return items


def _load_lang(path):
    LANG = {}
    for lang_path in lang.path:
        data_lang = _load(path + lang_path)
        LANG[data_lang["identify"]] = data_lang
    return LANG


def _entity_data(path):
    DATA = _load(path)

    list_of_stats: list = []
    for _, name in DATA["entity_values"].items():
        list_of_stats.extend(name)

    DATA["stats"] = list_of_stats
    DATA["all_stats"] = list_of_stats.copy() + ["_max_" + name for name in DATA["entity_values"]["resource"]]

    return DATA


if __name__ == '__main__':
    Game = json.dumps(_init(), indent=4)
    print(Game)
    with open("file_game.json", "w") as f:
        f.write(Game)