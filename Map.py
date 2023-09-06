from Constant import *
import queue
import random


class Map:
	def __init__(self):
		self.n = self.m = None
		self.reborn_R = self.reborn_C = None
		self.r = self.c = None
		self.layer = None
		self.mp = None
		self.fog = None
		self.npc = None

	def in_dirt(self, r, c):
		return 1 <= r <= self.n and 1 <= c <= self.m

	def in_map(self, r, c):
		return 0 <= r <= self.n and 1 <= c <= self.m

	def in_shop(self, tp, r, c):
		return self.mp[r][c] == tp

	def in_under(self, r, c):
		return 1 <= r <= self.layer[3] and 1 <= c <= self.m

	def in_cave(self, r, c):
		return self.layer[3] < r <= self.n and 1 <= c <= self.m

	def in_bound_r(self, r):
		return 0 <= r <= self.n - SCR_CEN_R + 1

	def in_bound_c(self, c):
		return SCR_CEN_C <= c <= self.m - SCR_CEN_C + 1

	def init_new(self):
		self.n, self.m = MAP_N, MAP_M

		self.reborn_R, self.reborn_C = 0, self.m // 2 + 1
		self.r, self.c = self.reborn_R, self.reborn_C

		self.layer = [0]
		for i in range(0, DIRT_TOT):
			self.layer.append(self.layer[0] + self.n * (i + 1) // DIRT_TOT)

		self.mp = [[] for i in range(0, self.n + 1)]
		self.fog = [[1] * (self.m + 1) for i in range(0, self.n + 1)]
		self.npc = {}
		for npc in NPCS:
			self.npc[npc] = 0
		self.__generate_map()

	def __grow_ore(self, ore, sz, row, col):
		Q = queue.Queue()
		if row == 1:
			return
		Q.put([row, col])
		self.mp[row][col] = ore
		sz -= 1
		while not Q.empty() and sz > 0:
			r, c = Q.get()
			for dr, dc in [D_XY[D_U], D_XY[D_D], D_XY[D_L], D_XY[D_R]]:
				nr, nc = r + dr, c + dc
				if not self.in_dirt(nr, nc) or nr == 1:
					continue
				rnd = random.randint(1, ORE_GROW_K[1])
				if rnd > ORE_GROW_K[0]:
					continue
				Q.put([nr, nc])
				self.mp[nr][nc] = ore
				sz -= 1
				if sz == 0:
					break

	def __generate_ore(self, ore, range):
		sz = random.randint(BLK_DATA[ore]['sz'] * ORE_MINSZ_K[0] // ORE_MINSZ_K[1], BLK_DATA[ore]['sz'])
		row = random.randint(range[0], range[1])
		col = random.randint(1, self.m)
		self.__grow_ore(ore, sz, row, col)

	def __generate_chest(self, chest, range):
		row = random.randint(range[0] + 1, range[1])
		col = random.randint(1, self.m)
		self.mp[row][col] = chest

	def __npc_too_close(self, row, col):
		for i in range(row - 2, row + 3):
			for j in range(col - 1, col + 2):
				if not self.in_dirt(i, j):
					continue
				if is_NPC(self.mp[i][j]):
					return 1
		return 0

	def __generate_npc(self, npc, range):
		row = random.randint(range[0] + 2, range[1])
		col = random.randint(1, self.m)
		while self.__npc_too_close(row, col):
			row = random.randint(range[0], range[1])
			col = random.randint(1, self.m)
		self.mp[row][col] = npc
		self.mp[row-1][col] = EMPTY

	def __generate_map(self):
		ore_range = {}
		for i in range(0, ORE_TOT):
			ore_range[ORES[i]] = [self.layer[i // 3] + 1, self.layer[i // 3 + 1]]
		chest_range = {}
		for i in range(0, CHEST_TOT):
			tmp = max(i // 2 - 1, 1) - 1
			chest_range[CHESTS[i]] = [self.layer[tmp] + 1, self.layer[tmp + 1]]
		npc_range = {}
		for i in range(0, NPC_TOT):
			tmp = min(i, 20)
			npc_range[NPCS[i]] = [self.layer[tmp // 3] + 1, self.layer[tmp // 3 + 1]]

		self.mp[0] = [EMPTY for i in range(0, self.m + 1)]
		for i in range(0, DIRT_TOT):
			ll, rr = self.layer[i] + 1, self.layer[i + 1]
			for j in range(ll, rr + 1):
				self.mp[j] = [DIRTS[i] for k in range(0, self.m + 1)]
		for ore in ORES:
			for i in range(0, BLK_DATA[ore]['num']):
				self.__generate_ore(ore, ore_range[ore])
		for chest in CHESTS:
			for i in range(0, BLK_DATA[chest]['num']):
				self.__generate_chest(chest, chest_range[chest])
		for npc in NPCS:
			self.__generate_npc(npc, npc_range[npc])

		for key, val in SHOP_R.items():
			for i in range(val[0], val[1] + 1):
				self.mp[0][i + self.reborn_C] = key
		for i in range(1, FOG_RAD + 1):
			self.fog[i] = [0] * (self.m + 1)

