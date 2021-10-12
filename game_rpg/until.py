import random


def set_multiple_attributes(object_, **kwargs):
    for key, value in kwargs.items():
        setattr(object_, key, value)


def add_multiple_attributes(object_, **attribute):
    for name_key, value in attribute.items():
        if isinstance(value, int):
            value = getattr(object_, name_key, 0) + value
        setattr(object_, name_key, value)


def resolve_index_condition(index, data: dict):
    print(f"resolve_index_condition -- fuction -- {__file__}")
    for key, value in data.items():
        if key == index:
            return value
    else:
        return


def resolve_random_condition(chances_data: list):
    """
    Example:
    -------
          print(resolve_random_condition([
         (True, 20.1),
         (1, 10)
         ]))
    """

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
    """
    Generate a random integer or float between 1 and the given limit inclusive.

    Arguments
    ---------
        upper_limit : int, float
            The upper limit of random numbers to generate.
        """
    if isinstance(upper_limit, float):
        return round(random.uniform(1, upper_limit), 2)
    else:
        return random.randint(1, upper_limit)


def clamp(x, min_x, max_x):
    return max(min_x, min(x, max_x))

