from .interface import get_messages
from .until import set_multiple_attributes
from statistics import fmean


class Attack:
    def __init__(
        self,
        name,
        identify,
        damage,
        description_of_being_used,
        type_damage,
        type_attack,
        cost_mp=0,
        cost_st=0,
        raw_attack=1, # default 1
        countdown=0,
        effect=None,
        multiplier_damage=None
    ) -> None:
        
        if not isinstance(damage, (list)):
            damage = [damage, damage]

        if not effect:
            effect = []

        if not multiplier_damage:
            multiplier_damage = []

        set_multiple_attributes(
            self,
            name=name,
            identify=identify,
            damage=damage,
            description_of_being_used=description_of_being_used,
            type_damage=type_damage,
            type_attack=type_attack,
            cost_mp=cost_mp,
            cost_st=cost_st,
            raw_attack=raw_attack,
            countdown=countdown,
            effect=effect,
            multiplier_damage=multiplier_damage,
            cooldown=countdown
        )
    
    def generate_damage(self, attacker, enemy) -> list:
        damage = []
        multiplier = self.multiplier_damage
        for dmg in self.damage:
            if isinstance(dmg, dict):
                damage.append(modifier_damage(dmg, attacker, enemy))
            if isinstance(dmg, (int, float)):
                damage.append(dmg)
        if multiplier and isinstance(multiplier, dict):
            damage_multiplier = modifier_damage(multiplier, attacker, enemy)
            damage = [min(damage) + damage_multiplier, max(damage) + damage_multiplier]

        if multiplier and isinstance(multiplier, list):
            for name in multiplier:
                damage_multiplier = modifier_damage(name, attacker, enemy)
                damage = [min(damage) + damage_multiplier, max(damage) + damage_multiplier]
        return sorted(damage)


    @classmethod
    def load_attack(cls, data: dict):
        if not isinstance(data, dict):
            return

        countdown = data.get("countdown", 0)
        if countdown > 0:
            countdown += 1

        return cls(
            name=data["name"],
            identify=data.get("identify"),
            damage=data["damage"],
            description_of_being_used=get_messages(
                data["description_of_being_used"], data["description_of_being_used"]
            ).format( name=data["name"].lower() ),
            type_damage=data["type_damage"],
            type_attack=data.get("type_attack", data["identify"].split(".")[0]),
            cost_mp=data.get("cost_mp", 0),
            cost_st=data.get("cost_st", 0),
            raw_attack=data.get("raw_attack", 1),
            countdown=countdown,
            effect=data.get("effect", []),
            multiplier_damage=data["multiplier_damage"]
        )


def modifier_damage(damage: dict, attacker, enemy) -> int | float:
    value = damage["value"]
    modifier = damage["modifier"]

    if isinstance(value, str):
        value = value.split(".")
        if value[0] == "enemy":
            value = getattr(enemy, value[1])
        elif value[0] == "self":
            value = getattr(attacker, value[1])
    
    if isinstance(value, dict):
        value = value.get("attacker.typeAttack", value)

    if isinstance(value, (int, float)):
        value *= modifier
    
    if isinstance(value, list):
        value = fmean(value) * modifier

    if not isinstance(value, (int, float)):
        value = 1
    return round(value)
