# from .data import DATA
from . import view, battle_util, player_turn, player_attack_phase, enemy_attack_phase
from .. import namespace, interface, util

class Battle:
    def __init__(self, player, enemy) -> None:

        self.player = player
        self.enemy = enemy
        self.loot = enemy.looting
        self.fled = False
        self.max_use_items = 3
        self.count_use_items = 0
        self.count_turn_battle = 0
        self.count_crit_player = 0
        self.count_dodge_player = 0
        self.__width_line = 55

    @property
    def width_line(self):
        return util.clamp(self.__width_line, 50, self.__width_line)

    def run(self):
        while self.enemy:

            self.turn_run()

            if self.fled:
                return namespace.BATTLE_FLED

            if self.player.health < 1:
                return namespace.BATTLE_LOSE

            if self.enemy.health < 1:
                return namespace.BATTLE_WIN

    def turn_run(self):
        self.player_turn()
        self.update_cooldown_of_attack(self.player)
        self.count_turn_battle += 0.5

        interface.centerprint("-", width=self.width_line)
        if self.fled or self.enemy.health < 1:
            return

        self.enemy_attack_phase()
        interface.print_("\n")
        self.update_cooldown_of_attack(self.enemy)
        self.count_turn_battle += 0.5

    view = view.view
    get_prefixes = battle_util.get_prefixes
    print_message = battle_util.print_message
    print_deal_damage = battle_util.print_deal_damage
    update_cooldown_of_attack = battle_util.update_cooldown_of_attack
    print_list_of_attacks_player = battle_util.print_list_of_attacks_player
    player_turn = player_turn.player_turn
    player_attack_phase = player_attack_phase.player_attack_phase
    enemy_attack_phase = enemy_attack_phase.enemy_attack_phase
