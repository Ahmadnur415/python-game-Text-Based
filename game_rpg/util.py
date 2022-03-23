import random


def generate_level(lv: int, diff: int=1) -> int:
    from .entity import DATA as dt

    if 3 < lv <= 7:
        lv = (1, lv)
    elif lv > 7:
        if lv < dt["max_level"] - 3:
            max_lv = clamp(lv + diff, 1, dt["max_level"])
            lv = (lv - int(4  - (1.5 * diff)) , max_lv)
        elif lv >= 57:
            lv = (57 - int(4  - (1.5 * diff)), lv)

    if isinstance(lv, tuple):
        lv = random.randrange(lv[0], lv[1])

    return lv


def resolve_random_condition(chances_data: list):
    sum_of_chances = sum([
        individual_chance_data[1] for individual_chance_data in chances_data
    ])
    random_value = _generate_random_value(sum_of_chances)
    range_checked = 0

    for individual_chance_data in chances_data:
        key, chance = individual_chance_data
        range_checked += chance
        if random_value <= range_checked:
            return key


def _generate_random_value(upper_limit):
    if isinstance(upper_limit, float):
        return round(random.uniform(1, upper_limit), 2)
    else:
        return random.randint(1, upper_limit)


def clamp(x, min_x, max_x):
    return max(min_x, min(x, max_x))


def _generate_value_from_dict(data: dict, self, enemy):
    # format dict { "modiefer": 1, "equal": "self.level", "percent": bool, "base_value": 10, "max_value": 30}
    value = 1
    def _value(prefix: str):
        prefix, stat = prefix.split(".")
        return getattr(enemy if prefix == "enemy" else self, stat, 1)

    if isinstance(data['equal'], str):
        value = _value(data["equal"])

    if isinstance(value, (int, float)):
        # modifier
        modiefer = data["modiefer"]
        if isinstance(modiefer, str):
            modiefer = _value(modiefer)

        value = value * modiefer
        if data.get("percent"):
            value /= 100

        if data.get("base_value"):
            value += data["base_value"]

        if data.get("max_value"):
            value = clamp(value, value, data["max_value"])

        return round(value, 0)
    raise ValueError(f"type {type(value)} : {str(value)} --- data {data}")


def short_stat(stat: str):
    from .interface.get_messages import get_messages
    return get_messages("short_name." + stat, stat.capitalize())


def generate_rows_list(index: int, data: list) -> list:
    rows = []

    while data != []:
        rows.append(data[:index])
        data = data[index:]

    return rows
