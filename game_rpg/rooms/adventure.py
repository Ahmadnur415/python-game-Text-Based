from ..import enemies, battle, interface
from ..items import get_items, Items as ITEMS
from ..room import Room
from ..until import resolve_random_condition
import random


def enter(self, game):
    if not (self.enemy and isinstance(self.enemy, enemies.Enemy)):
        self.enemy = enemies.enemyRandom(
            enemies._generate_enemy_level(game.player.level, game.setting["difficulty"]))
    Battle = battle.Battle(game.player, self.enemy)
    result_battle = Battle.run()

    # print result battle
    print()
    
    if result_battle != "fled":
        Battle.view_battle()
        interface.centerprint("-")
        
        modifier = 1 if result_battle == "win" else 0.5

        # menerima hadiah
        exp = int(Battle.count_turn * 10 * modifier)
        gold = int((Battle.count_crit * 2 + Battle.count_turn / 2 + Battle.count_dodge / 5) * modifier)
        silver = int((Battle.count_turn * 100 + (Battle.count_crit + Battle.count_dodge) / 4) * modifier)

        game.player.gain_exp(exp)
        game.player.gold += gold
        game.player.silver += silver

        interface.centerprint(
            "--" + interface.get_messages(f"battle.{result_battle}") + " --",
            interface.get_messages("battle.loot").format(
                f"{exp} exp, {gold} gold, and {silver} silver"
            )
        )

        if result_battle != "win":
            interface.get_enter()

    if result_battle == "win":

        # get looting
        if not self.enemy.looting:
            pass

        looting = resolve_random_condition(self.enemy.looting)
        if "#" in looting:
            name, value = looting.split("#")
            try:
                value = int(value)
            except ValueError:
                pass

            setattr(game.player, name, getattr(game.player, name) + value)
            interface.centerprint(
                interface.get_messages("battle.loot").format(
                    f"{value} {name}"
                )
            )
        if ":" in looting:
            items = get_items(looting)
            if isinstance(items, ITEMS):
                game.player.append_inventory(items)

                interface.centerprint(
                    interface.get_messages("battle.loot").format(
                        items.name
                    )
                )    

        print()
        interface.get_enter()


    self.enemy = None
    return "main"

ROOM = Room(
    "adventure",
    enter=enter,
    commands=None,
    enemy=None,
    loot_create=[]
)