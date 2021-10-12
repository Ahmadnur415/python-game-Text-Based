from .. import until
from . import view, run as RUN, battle_util, command, player_turn, enemy_turn


class Battle:
    def __init__(self, player, enemy, loot_table=None):
        if not loot_table:
            loot_table = []

        until.set_multiple_attributes(
            self,
            player=player,
            enemy=enemy,
            first_turn=True,
            entities=[player, enemy],
            fled=False,
            count_turn=0,
            count_crit=0,
            count_dodge=0
        )

    FLED = command.FLED
    ATTACK = command.ATTACK
    USE_ITEMS = command.USE_ITEMS
    BACK = command.BACK
    WIN = command.WIN
    LOSE = command.LOSE
    TURN_COMMANDS = command.TURN_COMMANDS

    view_battle = view.view_battle

    run = RUN.run
    run_turn = RUN.run_turn
    run_player_turn = player_turn.run_player_turn
    run_enemy_turn = enemy_turn.run_enemy_turn

    print_list_of_attacks = battle_util.print_list_of_attacks
    _list_of_attacks_player = battle_util._list_of_attacks_player

    player_attack_phase = player_turn.player_attack_phase