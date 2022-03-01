from .. import interface

def print_list_of_attacks_player(battle):
    interface.print_title("list of Attack", battle.width_line)

    distance = 5
    for i, attack in enumerate(battle.player.attacks):
        interface.leftprint(
            "{:>2}) {}".format(i + 1, attack.name),
            distance=0
        )

        interface.leftprint(
            interface.get_messages("attack.cooldown").format(attack.cooldown),
            interface.get_messages("attack.mana_cost_template").format(attack.cost_mana),
            interface.get_messages("attack.stamina_cost_template").format(attack.cost_stamina),
            distance=distance,
            width=battle.width_line
        )


def print_message(battle, message: str, *args, **kwargs):
    interface.centerprint(
        interface.get_messages("battle.message." + message).format(*args, **kwargs),
        width=battle.width_line
    )


def print_deal_damage(battle, enemy, attack, damage):

    entity = battle.player

    if enemy._namespace != battle.enemy._namespace:
        entity = battle.enemy

    battle.print_message(
        "damage_dealt",
        attacker=battle.get_prefixes(entity),
        attack_description=attack.description_of_being_used,
        enemy=battle.get_prefixes(enemy),
        damage=damage,
        type_damage=attack.type_damage
    )


def get_prefixes(battle, entity) -> str:

    if entity._namespace == battle.enemy._namespace:
        return interface.get_messages("battle.prefixes.enemy")

    return interface.get_messages("battle.prefixes.player")


def update_cooldown_of_attack(_, entity):
    for attack in entity.attacks:
        if attack.cooldown > 0:
            attack.cooldown -= 1
