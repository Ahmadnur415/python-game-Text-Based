from .game import Game
from .. import enemies, interface, namespace, util
from ..battle import Battle
from ..item import get_items
import random

def enter(_, player):

    enemy = enemies.create_enemy_random(util.generate_level(player.level, player.dificulty))

    battle = Battle(player, enemy)
    result_battle = battle.run()

    if result_battle == namespace.BATTLE_FLED:
        interface.get_messages("")

        from .main import main as main_menu
        return main_menu.enter(player)

    interface.print_("\n")
    battle.view()
    player.message_width_for_lv = battle.width_line
    interface.print_title("battle_" + result_battle.lower(), battle.width_line)

    modifier = 1
    bonus = 10 + 10 * (enemy.level - player.level)
    if result_battle == namespace.BATTLE_LOSE:
        modifier = 0.5
        bonus /= 2

    exp = int(100 * modifier + battle.count_turn_battle * 35)
    gold = int((battle.count_turn_battle / 4 + \
        battle.count_crit_player * 3 + \
        battle.count_dodge_player * 5 * modifier) + (1 if result_battle == namespace.BATTLE_LOSE else 5))

    silver = int((battle.count_turn_battle * 100 + \
        battle.count_crit_player * 50 + \
        battle.count_dodge_player * 25 * modifier) + (100 if result_battle == namespace.BATTLE_LOSE else 250))

    exp += int(exp / 100 * bonus)
    gold += int(gold / 100 * bonus)
    silver += int(silver / 100 * bonus)

    interface.centerprint(
        interface.get_messages("battle.get_basic_loot").format(exp=exp, gold=gold, silver=silver),
        width=battle.width_line
    )

    player.exp += exp
    player.gold += gold
    player.silver += silver

    if result_battle == namespace.BATTLE_WIN:
        loot = util.resolve_random_condition(battle.loot.copy())
        loot_id = loot["id"]
        amount = loot["value"]

        if isinstance(amount, list):
            amount = random.randrange(amount[0], amount[1])

        if loot_id in ["silver", "gold"]:
            setattr(
                player, loot_id, getattr(player, loot_id) + amount
            )
        else:
            item = get_items(loot_id)
            loot_id = item.name
            item.amount = amount
            player.add_items(item)

        interface.centerprint(
            interface.get_messages("battle.get_loot").format(amount=amount, name=loot_id),
            width=battle.width_line
        )

    interface.centerprint("-", interface.get_messages("input_messages.get_enter"), width=battle.width_line)
    input()
    interface.print_("\n")

    player.message_width_for_lv = 50

    from .main import main as main_menu
    return main_menu.enter(player)


main = Game(
    namespace.ADVENTURE,
    enter,
)
