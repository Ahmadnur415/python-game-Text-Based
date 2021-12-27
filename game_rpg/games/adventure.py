from ..import enemies, battle, interface, namespace
from ..items import get_items, Items as ITEMS
from .game import game as GAME
from ..until import resolve_random_condition
import random


def enter(self, game):
    if not (self.enemy and isinstance(self.enemy, enemies.Enemy)):
        self.enemy = enemies.enemyRandom(
            enemies._generate_enemy_level(game.player.level, game.setting["difficulty"]))
    Battle = battle.Battle(game.player, self.enemy)
    result_battle = Battle.run()

    print()
    for attack_player in game.player.attack:
        attack_player.cooldown = attack_player.countdown

    if result_battle != namespace.BATTLE_FLED:
        Battle.view_battle()
        interface.centerprint("-")
        
        modifier = 1 if result_battle == namespace.BATTLE_WIN else 0.5
        exp = int(Battle.total_turn_battle * 10 * modifier)
        gold = int((Battle.count_crit * 2 + Battle.total_turn_battle / 2 + Battle.count_dodge / 5) * modifier)
        silver = int((Battle.total_turn_battle * 100 + (Battle.count_crit + Battle.count_dodge) / 4) * modifier)

        game.player.gain_exp(exp)
        game.player.gold += gold
        game.player.silver += silver

        interface.centerprint(
            "--" + interface.get_messages(f"battle.{result_battle}") + " --",
            interface.get_messages("battle.loot").format(
                f"{exp} exp, {gold} gold, and {silver} silver"
            )
        )

        if result_battle != namespace.BATTLE_WIN:
            interface.get_enter()

    if result_battle == namespace.BATTLE_WIN:

        # get looting
        if not self.enemy.looting:
            pass

        loot = resolve_random_condition(self.enemy.looting)
        if isinstance(loot["value"], list):
            loot["value"] = random.randint(min(loot["value"]), max(loot["value"]))

        if loot["name"] in ("silver", "gold"):
            setattr( game.player, loot["name"], getattr(game.player, loot["name"]) + loot["value"] )
            interface.centerprint(interface.get_messages("battle.loot").format(f"{loot['value']} {loot['name']}"))
        else:
            items = get_items(loot["name"])
            if isinstance(items, ITEMS):
                items.amount = loot["value"]
                game.player.append_inventory(items)
                interface.centerprint(
                    interface.get_messages("battle.loot").format(
                        f"{loot['value']}x {items.name}" if loot["value"] > 1 else f"{items.name}"
                    )
                )

        print()
        interface.get_enter()


    self.enemy = None
    return "main"

main = GAME(
    "adventure",
    enter=enter,
    commands=None,
    enemy=None,
    loot_create=[]
)