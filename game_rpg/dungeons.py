import random
from .util import clamp, resolve_random_condition
from .enemies import create_enemy_random
from .battle import Battle
from .item import get_items
from . import namespace, interface


def create_wall(dungeons, wall, dirc):
	if dungeons.surrounding_wall(wall).count("c") < 2:
		dungeons.grid[wall[0]][wall[1]] = "c"

		def mark_new_walls(x, y):
			if dungeons.grid[x][y] != "c":
				dungeons.grid[x][y] = "w"

			if (x, y) not in dungeons.walls:
				dungeons.walls.append((x, y))

		if wall[0] != 0 and dirc != "down":
			mark_new_walls(wall[0]-1, wall[1])
		if wall[0] != dungeons.height - 1 and dirc != "up":
			mark_new_walls(wall[0]+1, wall[1])
		if wall[1] != 0 and dirc != "right":
			mark_new_walls(wall[0], wall[1]-1)
		if wall[1] != dungeons.width - 1 and dirc != "left":
			mark_new_walls(wall[0], wall[1]+1)

	if wall in dungeons.walls:
		dungeons.walls.remove(wall)


def generate_map(dungeons):
	dungeons.grid = [["u" for _ in range(dungeons.width)] for _ in range(dungeons.height)]
	start_x = clamp(random.randrange(dungeons.height), 1, dungeons.height - 2)
	start_y = clamp(random.randrange(dungeons.width), 1, dungeons.width - 2)

	dungeons.grid[start_x][start_y] = "c"
	dungeons.walls = [ (start_x + 1, start_y), (start_x - 1, start_y), (start_x, start_y + 1), (start_x, start_y - 1) ]

	for wall in dungeons.walls:
		dungeons.grid[wall[0]][wall[1]] = "w"

	while dungeons.walls:
		wall = random.choice(dungeons.walls)

		if wall[0] != 0 and dungeons.grid[wall[0]-1][wall[1]] == "u" and dungeons.grid[wall[0]+1][wall[1]] == "c":
			create_wall(dungeons, wall, "up")
			continue
		if wall[0] != dungeons.height - 1 and dungeons.grid[wall[0]+1][wall[1]] == "u" and dungeons.grid[wall[0]-1][wall[1]] == "c":
			create_wall(dungeons, wall, "down")
			continue
		if wall[1] != 0 and dungeons.grid[wall[0]][wall[1]-1] == "u" and dungeons.grid[wall[0]][wall[1]+1] == "c":
			create_wall(dungeons, wall, "left")
			continue
		if wall[1] != dungeons.width - 1 and dungeons.grid[wall[0]][wall[1]+1] == "u" and dungeons.grid[wall[0]][wall[1]-1] == "c":
			create_wall(dungeons, wall, "right")
			continue

		if wall in dungeons.walls:
			dungeons.walls.remove(wall)

	for i in range(0, dungeons.height):
		for j in range(0, dungeons.width):
			if dungeons.grid[i][j] == 'u':
				dungeons.grid[i][j] = 'w'

	# Set entrance and exit
	for i in range(0, dungeons.width):
		if dungeons.grid[1][i] == 'c':
			dungeons.grid[0][i] = 'c'
			dungeons.entrance = (0, i)
			break

	for i in range(dungeons.width-1, 0, -1):
		if (dungeons.grid[dungeons.height-2][i] == 'c'):
			dungeons.grid[dungeons.height-1][i] = 'c'
			dungeons.exit = (dungeons.height - 1, i)
			break

def generate(dungeons):
	generate_map(dungeons)

	count_enemy = 2 + (1 if dungeons.level % 5 else 0)
	count_loot = 1 + (1 if dungeons.level % 3 else 0)
	change_enemy = 3
	change_loot = 3

	x = 0
	for _ in range(0, 1000):
		if x == dungeons.height - 1:
			x = 0

		if count_enemy == 0:
			break

		for y in range(1, dungeons.width - 1):
			# set enemy
			if dungeons.surrounding_wall((x, y)).count("c") > 2 and dungeons.grid[x][y] == "c" and count_enemy > 0:
				drop = resolve_random_condition(sorted([
					(True, change_enemy),
					(False, 100 - change_enemy)
				], key=lambda d: d[1]))

				if f"{x}:{y}" not in dungeons.location_enemy and drop:
					dungeons.location_enemy[f"{x}:{y}"] = create_enemy_random(dungeons.level, False)# { "id": "enemy id", "level": dungeons.level}
					count_enemy -= 1
					change_enemy = 10
				else:
					change_enemy += 5

			# set loot
			if dungeons.surrounding_wall((x, y)).count("c") <= 2 and dungeons.grid[x][y] == "c" and count_loot > 0:
				drop = resolve_random_condition(sorted([
					(True, change_loot),
					(False, 100 - change_loot)
				], key=lambda d: d[1]))

				if f"{x}:{y}" not in dungeons.location_loot and drop:
					dungeons.location_loot[f"{x}:{y}"] = [looting()]
					count_loot -= 1
					change_loot = 10
				else:
					change_loot += 5
		x += 1

def looting():
	return [
		({"id": "silver", "value": 2500}, 25),
		({"id": "silver", "value": 5000}, 15),
		({"id": "food/banana", "value": [1, 3]}, 15),
		({"id": "food/apple", "value": [1, 3]}, 15),
		({"id": "gold", "value": 10}, 15),
		({"id": "helmet/sock", "value": 1}, 5),
		({"id": "gold", "value": 25}, 5),
		({"id": "silver", "value": [5000, 10000]}, 3),
		({"id": "bow/bow_of_storm", "value": 1}, 0.5),
		({"id": "sword/dragon_ice", "value": 1}, 0.5),
		({"id": "staff/fbi_staff", "value": 1}, 0.5),
		({"id": "gold", "value": [25, 100]}, 0.5)
	]


class Dungeons:
	def __init__(self, size: tuple | list, level: int):
		self.size = size
		self.height, self.width = self.size
		self.level = level
		self.grid = []
		self.entrance = None
		self.exit = None
		self.walls = []
		self.location_enemy = {}
		self.location_loot = {}
		self.position_x = 0
		self.position_y = 0

		generate(self)
		self.position_x, self.position_y = self.entrance

	def surrounding_wall(self, wall: tuple | list):
		return [
			self.grid[wall[0]+1][wall[1]],
			self.grid[wall[0]-1][wall[1]],
			self.grid[wall[0]][wall[1]-1],
			self.grid[wall[0]][wall[1]+1],
		]

	def reset(self):
		self.entrance = None
		self.exit = None
		self.location_enemy = {}
		self.location_loot = {}
		self.grid = []
		generate(self)
		self.position_x, self.position_y = self.entrance

	def next_map(self):
		if self.location_enemy:
			return 

		self.level += 1
		self.height += 1 if self.level % 3 == 0 else 0
		self.width += 1 if self.level % 5 == 0 else 0
		self.size = ( self.height, self.width )
		self.reset()


	def move(self, player, x, y):
		x = self.position_x + x
		y = self.position_y + y
		move = True

		t = f"{x}:{y}"

		if t in self.location_enemy:
			battle = self.location_enemy[t]
			if not isinstance(battle, Battle):
				battle = Battle(player, battle)
				self.location_enemy[t] = battle
			result = battle.run()
			interface.print_("\n")

			if result == namespace.BATTLE_WIN:
				self.location_enemy.pop(t)

				if t in self.location_loot:
					self.location_loot[t].append(battle.loot)
				else:
					self.location_loot[t] = [battle.loot]
			else:
				move = False
		if move:
			self.position_x = x
			self.position_y = y

		if (x, y) == self.exit:
			self.next_map()

	def printMaze(self):
		for i in range(0, self.height):
			for j in range(0, self.width):
				print(str(self.grid[i][j]), end=" ")

			print('')

	def looting(self, player):
		locate = f"{self.position_x}:{self.position_y}"
		if locate not in self.location_loot:
			return

		for loot in self.location_loot[locate]:
			loot = resolve_random_condition(loot)
			if isinstance(loot["value"], list):
				loot["value"] = random.randrange(loot["value"][0], loot["value"][1])

			if loot["id"] in ("silver", "gold"):
				setattr(
					player, loot["id"], getattr(player, loot["id"]) + loot["value"]
				)
			else:
				item = get_items(loot["id"], loot["value"])
				loot["id"] = item.name
				player.add_items(item)

			interface.centerprint(
				interface.get_messages("battle.get_loot").format(amount=loot["value"], name=loot["id"]),
			)
		self.location_loot.pop(locate)
		interface.get_enter()
