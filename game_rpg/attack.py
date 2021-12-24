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
        cost_st=0,
        countdown=None
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
            multiplier=multiplier,
            turn_count=countdown,
            countdown=countdown
        )


class Multiplier:
    def __init__(self, modifier, stats):
        self.modifier = modifier
        self.stats = stats


def ATTACK(data: dict):
    if not data or not isinstance(data, dict):
        return

    countdown = data.get("countdown", 0)
    if countdown > 0:
        countdown += 1

    return Attack(
        name=data["name"],
        displayName=data["displayName"],
        typeAttack=data["typeAttack"],
        base_damage=data.get("base_damage", 0),
        multiplier=None if not data["multiplier"] else [Multiplier(modifier=values["modifier"], stats=values["stats"])for values in data["multiplier"]],
        description_of_being_used=get_messages(data["description_of_being_used"], data["description_of_being_used"]).format(name=data["displayName"].lower()),
        cost_mp=data.get("cost_mp", 0),
        cost_st=data.get("cost_st", 0),
        countdown=countdown
    )
