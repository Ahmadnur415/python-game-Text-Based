from .. import interface


def view_battle(Battle):
    interface.centerprint(f"== {interface.get_messages('battle.title')} ==")
    print_line(
        [
            "Name : " + Battle.player.name,
            interface.get_messages("view.health") + " : " + str(Battle.player.health) + " / " + str(Battle.player.max_health),
            interface.get_messages("view.mana") + " : " + str(Battle.player.mana) + " / " + str(Battle.player.max_mana),
            interface.get_messages("view.stamina") + " : " + str(Battle.player.stamina) + " / " + str(Battle.player.max_stamina),
            "Class : " + Battle.player._class
        ],
        [
            Battle.enemy.name + " : Name",
            str(Battle.enemy.health) + " / " + str(Battle.enemy.max_health) + " : " + interface.get_messages("view.health"),
            str(Battle.enemy.mana) + " / " + str(Battle.enemy.max_mana) + " : " + interface.get_messages("view.mana"),
            str(Battle.enemy.stamina) + " / " + str(Battle.enemy.max_stamina) + " : " + interface.get_messages("view.stamina"),
            Battle.enemy._class + " : Class"
        ]
    )


def print_line(left: list, right: list, distance=1):
    for a, b in zip(left, right):
        interface.LeftRigthPrint(left=a, right=b, distance=distance)
