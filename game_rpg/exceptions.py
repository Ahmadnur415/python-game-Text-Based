class GameError(Exception):
    ...


class EntityError(GameError):
    ...


class PlayerError(EntityError):
    ...


class EntityValuesFullError(EntityError):
    ...


class IlegalEquipItemError(EntityError):
    ...


class ItemAlreadyUsedError(EntityError):
    ...


class CantRemoveItemError(GameError):
    ...


class ItemNotInInventoryError(GameError):
    ...
