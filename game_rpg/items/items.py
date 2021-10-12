from .. import until, setup
from . import view


class Items:
    def __init__(
            self,
            name: str, 
            quality: str,
            typeItems: str,
            identify: int,
            attribute: object,
            amount: int = 1,
            price: dict = None,
            sub_stats: object = None,
            **other
    ):

        if not sub_stats:
            sub_stats = {}
        if not price:
            price = {"value": 10, "type": "gold", "max_discount": 30}

        until.set_multiple_attributes(
            self,
            name=name,
            quality=quality,
            typeItems=typeItems,
            identify=identify,
            attribute=attribute,
            amount=amount,
            price=price,
            sub_stats=sub_stats
        )
        until.set_multiple_attributes( self, **other )

    @property
    def namespace(self):
        return getattr(self.attribute, "namespace", None)

    @property
    def get_quality(self):
        return setup.DATA_ITEMS["quality"][self.quality]

    view_stats = view.view_stats


class EQUIPPABLE:
    namespace = "EQUIPPABLE"

    def __init__(
            self,
            location,
            user,
            styleAttack=None,
            attack=None,
            classItems=None,
            **stats
    ):
        if not attack:
            attack = []

        until.set_multiple_attributes(
            self,
            use=False,
            location=location,
            user=user,
            styleAttack=styleAttack,
            attack=attack,
            classItems=classItems
        )
        until.set_multiple_attributes(self, **stats)


class CONSUMABLE:
    namespace = "CONSUMABLE"

    def __init__(self, type_, stats, effect=None):
        if not effect:
            effect = []

        self.effect = effect

        until.set_multiple_attributes(self, type_=type_, stats=stats)
