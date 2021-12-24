from game_rpg.entity.other_property import damage
from ..import interface


def _list_of_attacks_player(battle, show_number=False) -> list:
    distance = 1 if not show_number else 3
    new_line = "\n" + " " * distance + " - "
    lines = []
    for i, attack in enumerate(battle.player.attack):

        damage = " ~ ".join([str(i) for i in battle.player._generate_damage_of_attack_use(battle.enemy, attack)])
        line = " " + attack.displayName + f" - {interface.get_messages(attack.typeAttack, attack.typeAttack)} damage: " + damage

        if show_number:
            line = "(" + str(i+1) + ")" + line

        if attack.turn_count >= attack.countdown:
            if attack.cost_st > 0:
                line += new_line + interface.get_messages("attack.stamina_cost_template").format(cost=attack.cost_st)
            
            if attack.cost_mp > 0:
                line += new_line + interface.get_messages("attack.mana_cost_template").format(cost=attack.cost_mp)
        
        if attack.turn_count < attack.countdown:
            line += new_line + interface.get_messages("attack.is_cooldown").format(value=attack.countdown - attack.turn_count)

        lines.append(line)
    return lines


def print_list_of_attacks(battle):
    interface.centerprint("== ATTACK ==")
    for line in battle._list_of_attacks_player(True):
        print(line)