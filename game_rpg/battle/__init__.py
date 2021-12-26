from .. import until, namespace
from . import view, battle_util, player_turn, enemy_turn


class Battle:
    def __init__(self, player, enemy, loot_table=None):
        if not loot_table:
            loot_table = []

        until.set_multiple_attributes(
            self,
            player=player,
            enemy=enemy,
            first_turn=True,
            fled=False,
            attack_trun=0,
            count_crit=0,
            count_dodge=0
        )

    def run(self):
        while True:
            
            self.run_trun()

            if self.fled:
                return namespace.BATTLE_FLED
            
            if self.player.health < 1:
                return namespace.BATTLE_LOSE

            if self.enemy.health < 1:
                return namespace.BATTLE_WIN

    def run_trun(self):
        self.run_player_turn()
        self.attack_trun += 1
        self.player.attack_turn_count()
        
        if self.fled or self.enemy.health < 1:
            return

        self.run_enemy_turn()
        self.enemy.attack_turn_count()

    view_battle = view.view_battle

    run_player_turn = player_turn.run_player_turn
    run_enemy_turn = enemy_turn.run_enemy_turn

    print_list_of_attacks = battle_util.print_list_of_attacks
    _list_of_attacks_player = battle_util._list_of_attacks_player

    player_attack_phase = player_turn.player_attack_phase