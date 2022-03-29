from copy import deepcopy
from .game import Game
from ..dungeons import Dungeons
from ..namespace import DIRECTION, BACK, DUNGEONS, LOOT
from .. import interface


def enter(self, player):
    if not player.dungeons:
        player.dungeons = Dungeons((10, 10), 1)
    dungeons = player.dungeons
    while True:
        lines = deepcopy(self.lines)
        list_option, moves = [], []
        x, y = dungeons.position_x, dungeons.position_y
        grid = dungeons.grid

        interface.print_title(self.name + f" {dungeons.level}", self.width)
        interface.leftprint("-"*(self.width - 1))
        interface.generates_readable_stats({
            interface.get_messages("game.dungeons.enemy_location") : ", ".join(["({}, {})".format(*t.split(":")) for t in list(dungeons.location_enemy.keys())]),
            interface.get_messages("game.dungeons.exit_location") : "({}, {})".format(*dungeons.exit),
            interface.get_messages("game.dungeons.player_location") : f"({x}, {y})"
        }, 1, self.width, one_line=True, use_sign=False)
        interface.leftprint("-"*(self.width - 1))

        if x - 1 > 0 and grid[x-1][y] == "c":
            list_option.append(f" n) {DIRECTION.NORTH}")
            moves.append(DIRECTION.NORTH)
            lines[DIRECTION.NORTH].insert(0, DIRECTION.NORTH + f"({x-1},{y})")

        if y - 1 > 0 and grid[x][y-1] == "c":
            list_option.append(f" w) {DIRECTION.WEST}")
            moves.append(DIRECTION.WEST)
            lines[DIRECTION.WEST] = f"{DIRECTION.WEST + f'({x}, {y-1})':>17} │"

        if y + 1 < dungeons.width and grid[x][y+1] == "c":
            list_option.append(f" e) {DIRECTION.EAST}")
            moves.append(DIRECTION.EAST)
            lines[DIRECTION.EAST] += " " + DIRECTION.EAST + f" ({x}, {y+1})"

        if x + 1 < dungeons.height and grid[x+1][y] == "c":
            list_option.append(f" s) {DIRECTION.SOUTH}")
            moves.append(DIRECTION.SOUTH)
            lines[DIRECTION.SOUTH].append(f"{DIRECTION.SOUTH} ({x+1}, {y})")

        interface.centerprint(*lines[DIRECTION.NORTH], width=self.width)
        interface.leftprint(lines[DIRECTION.WEST], width=self.width)
        interface.centerprint(lines["line"], width=self.width)
        interface.leftprint(lines[DIRECTION.EAST], width=self.width)
        interface.centerprint(*lines[DIRECTION.SOUTH], width=self.width)

        list_option.append(f" b) {BACK}")
        if f"{x}:{y}" in dungeons.location_loot:
            list_option.append(f" l) {LOOT}")

        interface.leftprint(
            interface.get_messages("game.dungeons.move"),
            *interface.generate_readable_list(list_option, number=False, make_line=False)
        )
        index = interface.get_input()

        interface.print_("\n")
        if index not in self.commands:
            continue

        if self.commands[index] in moves:
            _x, _y = self.moves[self.commands[index]]
            dungeons.move(player, _x, _y)

        if self.commands[index] == BACK:
            from .main import main as main_menu
            return main_menu.enter(player)

        if self.commands[index] == LOOT:
            dungeons.looting(player)

main = Game(
    DUNGEONS,
    enter,
    dungeons=None,
    width=40,
    moves={DIRECTION.NORTH: (-1, 0), DIRECTION.SOUTH: (1, 0), DIRECTION.WEST: (0, -1), DIRECTION.EAST: (0, 1)},
    commands = {
        "n": DIRECTION.NORTH, "s": DIRECTION.SOUTH, "w": DIRECTION.WEST, "e": DIRECTION.EAST, "b": BACK, "l": LOOT
    }
)
setattr(
    main,
    "lines", {
        DIRECTION.NORTH: ["▲"] + ["│"] * 2,
        DIRECTION.SOUTH: ["│"] * 2 + ["▼"],
        DIRECTION.WEST: " " * round(main.width / 2 - 2) + "│",
        DIRECTION.EAST:  ("{:>" + str(round(main.width / 2 - 1)) + "}").format("│"),
        "line": "◄" + "─" * 8 + "┼" + "─" * 8 + "►"
    }
)