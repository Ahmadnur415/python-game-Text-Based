from dataclasses import asdict
from typing import Any, Dict

from pydantic.dataclasses import dataclass

from .utils import *


@dataclass
class BaseItem:
    id: str
    name: str
    price: int
    quality: ItemQuality
    sub_type: str
    description: str
    in_shop: bool

    @property
    def type(self) -> "ItemType":
        raise NotImplementedError

    @type.setter
    def type(self, value: "ItemType"):
        raise NotImplementedError

    def dict(self) -> Dict[str, Any]:
        return asdict(self)

    @property
    def stackable(self):
        return True

    @stackable.setter
    def stackable(self):
        raise NotImplementedError
