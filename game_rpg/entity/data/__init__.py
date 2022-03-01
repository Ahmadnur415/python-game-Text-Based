import json
import os


DATA = json.load(
    open(
        os.path.dirname(
            os.path.realpath(__file__)
        ) + "/data.json"
    )
)


def _stats_entity():
    list_of_stats = []

    for stats in DATA["values"]:
        if stats == "resource":
            list_of_stats.extend(
                [ "_max_" + value_name for value_name in DATA["values"][stats]]
            )
        
        if stats == "critical":
            list_of_stats.extend(
                [ "_" + value_name for value_name in DATA["values"]["critical"]]
            )
            continue

        list_of_stats.extend(
            DATA["values"][stats].copy()
        )

    return list_of_stats


DATA["stats"] = _stats_entity()


def _full_stats():
    values = DATA["stats"].copy()
    values.extend( "_" + name for name in DATA["values"]["resource"])
    
    return values


DATA["full_stats"] = _full_stats()


def _full_equipment_entity():
    equipments = {}
    for name in DATA["equipment"].keys():
        equipments.update(
            dict.fromkeys(DATA["equipment"][str(name)])
        )
    
    return equipments


DATA["full_equipment"] = _full_equipment_entity()