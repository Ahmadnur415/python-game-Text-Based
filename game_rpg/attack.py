from .setup import _ATTACK
from .interface import get_messages
from . import until



class Attack:
    def __init__(
            self,
            name,
            displayName,
            typeAttack,
            base_damage,
            multiplier=None,
            effect=None,
            description_of_being_used="",
            cost_mp=0,
            cost_st=0
    ):
        if not multiplier:
            multiplier = []

        if not effect:
            effect = []

        until.set_multiple_attributes(
            self,
            name=name,
            displayName=displayName,
            typeAttack=typeAttack,
            base_damage=base_damage,
            description_of_being_used=description_of_being_used,
            cost_mp=cost_mp,
            cost_st=cost_st,
            effect=effect,
            multiplier=multiplier
        )


class Multiplier:
    def __init__(self, modifier, stats):
        self.modifier = modifier
        self.stats = stats


class _attackstyle:
    def __init__(self, damage_stats):
        self.damage_stats = damage_stats


AttackStyle = {name: _attackstyle(damage_stats=stats) for name, stats in _ATTACK["style_attack"].items()}


def ATTACK(data: dict):
    if not data or not isinstance(data, dict):
        return

    return Attack(
        name=data["name"],
        displayName=data["displayName"],
        typeAttack=data["typeAttack"],
        base_damage=data.get("base_damage", 0),
        multiplier=None if not data["multiplier"] else [Multiplier(modifier=values["modifier"], stats=values["stats"])for values in data["multiplier"]],
        description_of_being_used=get_messages(data["description_of_being_used"], data["description_of_being_used"]).format(name=data["displayName"].lower()),
        cost_mp=data.get("cost_mp", 0),
        cost_st=data.get("cost_st", 0)

    )
