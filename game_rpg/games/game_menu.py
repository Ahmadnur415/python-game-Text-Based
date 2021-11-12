class game_menu(object):
    def __init__(self, name, enter, commands: list=None, **others) -> None:

        if not commands:
            commands = []

        self.name = name
        self.enter_func = enter
        self.commands = commands

        for names, value in others.items():
            setattr(self, names, value)

    def enter(self, game):
        return self.enter_func(self, game)
    
    def add_commands(self, *commands):
        for command in commands:
            self.commands.append(command)
