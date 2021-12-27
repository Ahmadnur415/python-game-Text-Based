from .. import until, setup, namespace as nms
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
        stats: object = None,
        **other
    ):

        if not stats:
            stats = {}
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
            stats=stats
        )
        until.set_multiple_attributes( self, **other )

    @property
    def namespace(self):
        return getattr(self.attribute, "namespace", None)

    @property
    def get_quality(self):
        return setup.GAME["quality"][self.quality]

    @classmethod
    def from_identify(cls, identify):
        pass
    
    def __repr__(self) -> str:
        return self.identify

    def __str__(self) -> str:
        return self.identify

    view_stats = view.view_stats


class EQUIPPABLE:
    namespace = nms.EQUIPPABLE
    def __init__(self, location, user, styleAttack=None, attack=None, **stats ):

        if not attack:
            attack = []

        until.set_multiple_attributes(
            self,
            use=False,
            location=location,
            user=user,
            styleAttack=styleAttack,
            attack=attack,
            location_equipment=None
        )
        until.set_multiple_attributes(self, **stats)


class CONSUMABLE:
    namespace = nms.CONSUMABLE

    def __init__(self, type_, stats, effect=None):
        if not effect:
            effect = []

        self.effect = effect

        until.set_multiple_attributes(self, type_=type_, stats=stats)
