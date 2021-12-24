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


def _load_items():
    items = {"id": [], "items_by_type": {}, "list": {}}
    if not items.get("list"): items["list"] = {}

    for path_items in item.list_items:
        # ==========
        try:
            index_items = _load("item/" + path_items)
        except (FileNotFoundError) as e:
            print(e.args[1], f": .\\{path_items}")
            continue
        # ==========

        items["list"][path_items] = {}
        for names, values in index_items["items"].items():
            identify = path_items + "/" + names
            values["identify"] = identify
            
            values["type_items"] = index_items["type_items"]
            values["class"] = index_items["class"]

            if index_items["class"] == "EQUIPPABLE":    
                if not values.get("location", None):
                    values["location"] = index_items["location"]

                if not values.get("user", None):
                    values["user"] = index_items["user"]

                if index_items["type_items"] == "weapons":
                    values["styleAttack"] = index_items["styleAttack"]
 
            if not items["items_by_type"].get(values["type_items"], None):
                items["items_by_type"][values["type_items"]] = []

            items["items_by_type"][values["type_items"]].append(identify)
            items["list"][path_items][names] = values
            items["id"].append(identify)
    return items


def _load_lang(path):
    LANG = {}
    for lang_path in lang.list_lang:
        data_lang = _load(path + lang_path)
        LANG[data_lang["identify"]] = data_lang
    return LANG


def _load_entity(path):
    DATA = _load(path)

    list_of_stats: list = []
    for _, name in DATA["entity_values"].items():
        list_of_stats.extend(name)

    DATA["stats"] = list_of_stats
    DATA["all_stats"] = list_of_stats.copy() + ["_max_" + name for name in DATA["entity_values"]["resource"]]

    return DATA
