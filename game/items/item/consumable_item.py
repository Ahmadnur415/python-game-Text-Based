from typing import Union

from pydantic.dataclasses import dataclass

from ..effect.effects import Decrease, Increase, Recovery
from .base import BaseItem
from .utils import ItemSubtypeConsumable, ItemType


@dataclass
class ConsumableItem(BaseItem):
    sub_type: ItemSubtypeConsumable
    effect: Union[Decrease, Increase, Recovery]

    @property
    def type(self) -> "ItemType":
        return ItemType.CONSUMABLE

    def use(self, *args, **kwargs):
        return self.effect.apply(*args, **kwargs)
