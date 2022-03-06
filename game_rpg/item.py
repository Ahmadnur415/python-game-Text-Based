from copy import deepcopy
from .items import DATA
from . import interface, namespace
from .attack import generate_attack_for_items


class Item:
    def __init__(
        self,
        name: str,
        quality: int,
        class_item: str,
        identify: str,
        amount: int = 1,
        stats: dict | None = None,
        equip_location: str | None = None,
        attacks: list | None = None,
        effects: dict | None = None,
        price: dict | None = None,
        type_item: str | None = None,
        description: str | None = None,
        user: str | None = None
    ):

        if not effects:
            effects = {}

        if not stats:
            stats = { "basic": {}, "other": {} }

        if not user:
            user = []

        self.name = name
        self._quality = quality
        self.class_item = class_item
        self.identify = identify
        self.amount = amount
        self.equip_location = equip_location
        self.attacks = attacks
        self.price = price
        self.effects = effects
        self.type_item = type_item
        self.used = False
        self.location_used = None
        self.stats = stats
        self.description = description
        self.user = user

    def __repr__(self) -> str:
        return f"Item({self.identify})"

    @property
    def selling_price(self):
        return [int(self.price[0] * 0.8), self.price[1]]

    @property
    def quality(self):
        return namespace.LIST_OF_QUALITY[self._quality]

    def view(self):
        title = self.name
        if self.class_item == namespace.EQUIPPABLE and self.used:
            title += " [E]"

        if self.class_item == namespace.CONSUMABLE and self.amount > 1:
            title += f" {self.amount}x"

        interface.print_title( title )

        if self.class_item == namespace.EQUIPPABLE:
            desc = interface.get_messages("item.desc.equippable").format(
                interface.generate_readable_list(self.equip_location).replace("_", " ")
            )

        if self.class_item == namespace.CONSUMABLE:
            lines = []
            for name, value in self.effects["stats"].items():
                
                if isinstance(value, dict):
                    
                    if value.get("percent"):
                        lines.append(
                            interface.get_messages("item.desc.consumable.effect").format( stat=name, value=value["modiefer"], equal=value["equal"])
                        )
                    continue
                
                lines.append(str(value) + " " + name)

            desc = interface.get_messages("item.desc.consumable").format(
                interface.generate_readable_list(lines)
            )
        
        interface.print_message(
            "item.desc", "left", classitem=self.class_item.capitalize(), desc=desc, quality=self.quality
        )

        stats = deepcopy(self.stats)

        if stats:

            if self.stats.get("basic") and self.type_item == "weapons":

                interface.print_message("item.weapons_attribute", "left", " ~ ".join(str(i) for i in stats["basic"].get("damage", [0, 0])), stats["basic"]["armor_penetration"])

                stats["basic"].pop("damage")
                stats["basic"].pop("armor_penetration")

            for _, values in stats.items():
                interface.generates_readable_stats(
                    values, distance=2, use_colon=False, use_sign=True, one_line=True, use_prepix=True
                )


    @classmethod
    def _load_items(cls, _id: str, amount: int=1):
        if _id not in list(DATA["items"].keys()):
            raise NameError(f"Tidak ada id di DATA {_id}")

        item = DATA["items"][_id]
        item["id"] = _id

        return cls(
            name = item["name"],
            quality = item["quality"],
            class_item=item["type"],
            identify=_id,
            amount=amount,
            stats=item.get("stats"),
            equip_location=item.get("equip_location"),
            attacks=generate_attack_for_items(item),
            effects=item.get("effects", {}),
            price=item.get("price"),
            type_item=item["type_item"],
            description=item.get("description", ""),
            user=item.get("user", [])
        )

get_items = Item._load_items
