from .. import interface, setup


def view_battle(Battle):
    interface.centerprint(f"== {interface.get_messages('battle.title')} ==")
    view = setup.GAME["_view"].copy()
    print_line(
        [
            "Name : " + Battle.player.name,
            view["health"] + " : " + str(Battle.player.health) + " / " + str(Battle.player.max_health),
            view["mana"] + " : " + str(Battle.player.mana) + " / " + str(Battle.player.max_mana),
            view["stamina"] + " : " + str(Battle.player.stamina) + " / " + str(Battle.player.max_stamina),
            "Class : " + Battle.player._class
        ],
        [
            Battle.enemy.name + " : Name",
            str(Battle.enemy.health) + " / " + str(Battle.enemy.max_health) + " : " + view["health"],
            str(Battle.enemy.mana) + " / " + str(Battle.enemy.max_mana) + " : " + view["mana"],
            str(Battle.enemy.stamina) + " / " + str(Battle.enemy.max_stamina) + " : " + view["stamina"],
            Battle.enemy._class + " : Class"
        ]
    )


def print_line(left: list, right: list, distance=1):
    for a, b in zip(left, right):
        interface.LeftRigthPrint(left=a, right=b, distance=distance)
