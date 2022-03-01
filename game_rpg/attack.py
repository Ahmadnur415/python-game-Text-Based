from .data import _load
from . import util, interface

DATA = _load("attacks.json")


class Attack:
    def __init__(
        self,
        name,
        identify,
        damage,
        description_of_being_used,
        type_damage,
        type_attack,
        cost_mana=0,
        cost_stamina=0,
        countdown=0,
        effects=None,
        modiefer_damage=None

    ):
        if not isinstance(damage, (int, list)):
            damage = 1

        if not effects:
            effects = []

        self.effects = effects
        self.name = name
        self.identify = identify
        self.damage = damage
        self.type_damage = type_damage
        self.type_attack = type_attack
        self.countdown = countdown
        self.cooldown = 0
        self.modiefer_damage = modiefer_damage
        self.user = None
        self.__cost_mana = cost_mana
        self.__cost_stamina = cost_stamina
        self.description_of_being_used = interface.get_messages( "attack.desc." + description_of_being_used ).format(self.__dict__)

    def __repr__(self) -> str:
        return self.__class__.__name__ + "(" + self.identify + ")"

    def get_modiefer_damage(self, enemy):

        if not self.modiefer_damage:
            return 0

        if isinstance(self.modiefer_damage, dict) and self.user:
            return util._generate_value_from_dict(self.modiefer_damage, self.user, enemy)

        if isinstance(self.modiefer_damage, (int, float)):
            return self.modiefer_damage

        return 0

    @property
    def cost_mana(self):
        if isinstance(self.__cost_mana, dict) and self.user:
            return util._generate_value_from_dict(self.__cost_mana, self.user, self.user)

        if isinstance(self.__cost_mana, (int, float)):
            return self.__cost_mana

    @property
    def cost_stamina(self):
        if isinstance(self.__cost_stamina, dict) and self.user:
            return util._generate_value_from_dict(self.__cost_stamina, self.user, self.user)

        if isinstance(self.__cost_stamina, (int, float)):
            return self.__cost_stamina

    @classmethod
    def _load_attack_from_dict(cls, data):
        if not isinstance(data, dict):
            raise TypeError(f"TYPE ERROR {type(data)}")

        return cls(
            name=data["name"],
            identify=data.get("identify", data["name"]),
            damage=data.get("damage"),
            description_of_being_used=data["description_of_being_used"],
            type_damage=data["type_damage"],
            type_attack=data["type_attack"],
            cost_mana=data.get("cost_mana", 0),
            cost_stamina=data.get("cost_stamina", 0),
            countdown=data.get("countdown", 0),
            effects=data.get("effects"),
            modiefer_damage=data.get("modiefer_damage")
        )

    @classmethod
    def _load_attack_from_id(cls, _id):
        if _id not in DATA:
            raise NameError("ID SALAH")
        return cls._load_attack_from_dict(DATA[_id].copy() | {"identify": _id})


load_attack = Attack._load_attack_from_dict
load_from_id = Attack._load_attack_from_id


def generate_attack_for_items(item: dict):
    attacks = []

    if not item.get("stats") or item["type"] != "equippable" or not item.get("attacks"):
        return attacks

    for _id in item["attacks"]:

        if isinstance(_id, str) and _id in DATA:
            _attack = load_from_id(_id)

        elif isinstance(_id, dict):
            _attack = load_attack(_id)

        else:
            continue

        _attack.identify += "@" + item["id"]

        _attack.damage = item["stats"]["basic"].get("damage", [1,])

        attacks.append(_attack)

    return attacks
