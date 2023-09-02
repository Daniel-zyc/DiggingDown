from Constant import *
import queue


class Map:
	def __init__(self):
		self.n = self.m = None
		self.g_level = self.r_level = None
		self.dirt_L = self.dirt_R = self.dirt_U = self.dirt_D = None
		self.dirt_N = self.dirt_M = None
		self.reborn_R = self.reborn_C = None
		self.p_shop = self.g_shop = self.o_shop = self.d_shop = None
		self.layer = None
		self.mp = None

	def in_dirt(self, r, c):
		return self.dirt_U <= r <= self.dirt_D and self.dirt_L <= c <= self.dirt_R

	def in_bound(self, r, c):
		return self.in_dirt(r, c) or r == self.g_level or (r == self.r_level and c == self.reborn_C)

	def in_shop(self, tp, r, c):
		ll = self.reborn_C + SHOP_POS[tp]
		rr = ll + SHOP_W[tp] - 1
		return r == self.g_level and ll <= c <= rr

	def init_new(self):
		self.n, self.m, h = MAP_N, MAP_M, EMPTY_LAYER_H

		self.g_level = SCR_CEN_R
		self.r_level = self.g_level + 1

		self.dirt_U, self.dirt_D = self.r_level + 1, self.n
		self.dirt_L, self.dirt_R = 1, self.m
		self.dirt_N, self.dirt_M = self.dirt_D - self.dirt_U + 1, self.dirt_R - self.dirt_L + 1

		self.reborn_R, self.reborn_C = self.g_level, self.m // 2 + 1

		self.layer = [self.g_level + h]
		for i in range(0, ORES_TOT):
			self.layer.append(self.layer[0] + (self.dirt_N - h) * (i+1) // ORES_TOT)

		self.__generate_map()

	def __grow_ore(self, ore, sz, row, col):
		Q = queue.Queue()
		Q.put([row, col])
		self.mp[row][col] = ore
		sz -= 1
		while not Q.empty() and sz > 0:
			r, c = Q.get()
			for dr, dc in [D_XY[D_U], D_XY[D_D], D_XY[D_L], D_XY[D_R]]:
				nr, nc = r + dr, c + dc
				if not self.in_dirt(nr, nc):
					continue
				rnd = random.randint(1, 10)
				if rnd > BLK_DATA[ore]['grow']:
					continue
				Q.put([nr, nc])
				self.mp[nr][nc] = ore
				sz -= 1
				if sz == 0:
					break

	def __generate_ore(self, ore, range):
		sz = random.randint(BLK_DATA[ore]['min_sz'], BLK_DATA[ore]['sz'])
		row = random.randint(range[ore][0], range[ore][1])
		col = random.randint(self.dirt_L, self.dirt_R)
		self.__grow_ore(ore, sz, row, col)

	def __generate_map(self):
		ores_range = {}
		for i in range(0, ORES_TOT):
			ore = ORES[i]
			end = min(i+BLK_DATA[ore]['layer'], len(self.layer)-1)
			ores_range[ore] = [self.layer[i]+1, self.layer[end]]

		self.mp = [[DIRT] * (self.m + 1) for i in range(0, self.n + 1)]
		for i in range(0, self.g_level + 1):
			self.mp[i] = [EMPTY] * (self.m + 1)
		self.mp[self.r_level] = [ROAD] * (self.m + 1)
		self.mp[self.r_level][self.reborn_C] = DIRT
		for ore in ORES:
			for i in range(0, BLK_DATA[ore]['num']):
				self.__generate_ore(ore, ores_range)
