class Game:
    def __init__(self, name, enter, **kwargs) -> None:
        self.name = name
        self._enter = enter

        for name, value in kwargs.items():
            setattr(self, name, value)

    def enter(self, player):
        self._enter(self, player)

    def add_methode(self, name, func):
        setattr(self, name, func.__get__(self, self.__class__))
