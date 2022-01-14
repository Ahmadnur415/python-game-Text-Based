import os
import glob
import pickle
from datetime import datetime
from . import games, interface, create_player, setup, namespace


class Game:
    def __init__(self):
        self.player = None
        self.setting = None
        self.games = [games.main_menu.name, games.adventure.name, games.camp.name, games.shop.name, namespace.EXIT]

    def new_game(self):
        self.player = create_player.create_player()
        self.setting = setup.GAME["setting"].copy()
        self.setting["difficulty"] = create_player.select_dificulty()

    def start(self):
        if not self.player:
            self.new_game()

        setup.SETTING = self.setting

        return self.run()

    def run(self):
        if not self.player:
            return self.start()
        
        run = games.main_menu.name
        while True:
            if self.setting["auto_save"]:
                self.save_game()

            if run in (games.main_menu.name, "main"):
                run = games.main_menu.enter(self)
                continue

            if run == games.adventure.name:
                run = games.adventure.enter(self)
                continue
            
            if run == games.shop.name:
                run = games.shop.enter(self)
                continue

            if run == games.camp.name:
                run = games.camp.enter(self)
                continue

            if run == "exit":
                return quit()
        return quit()

    def save_game(self):
        path = "./saves/"
        if not self.setting["savename"]:
            name = self.player.name.replace(" ", "_") + ".sv"
            i = 0
            while name in os.listdir(path):
                name = self.player.name.replace(" ", "_") + f"_({i}).sv"
                i += 1
            self.setting["savename"] = name

        with open(path + self.setting["savename"], "wb") as f:
            pickle.dump(self, f, -1)


def load_game():
    games = []
    lines = []
    listSave = glob.glob("./saves/*.sv")
    
    # title
    interface.centerprint("== Load Game ==")
    print(f" {'No':<3}{'Name Player':<21}{'Level':<12}{'Time':<9}")

    for filename in listSave:
        try:
            game = pickle.load(open(filename, "rb"))
        except AttributeError:
            continue
        time_save = datetime.fromtimestamp(os.path.getmtime(filename)).strftime("%X %x")
        games.append(game)
        lines.append(" {:<3}" + f"{game.player.name:<21}{str(game.player.level).center(5):<12}{time_save:<9}")
    
    # no save file save
    if not games:
        interface.centerprint(interface.get_messages("game.no_file_save"))
        interface.get_enter()
        return "back"

    # display 
    for i, line in enumerate(lines):
        print(line.format(i+1))

    result_index = interface.get_command(games, False)
    return result_index
