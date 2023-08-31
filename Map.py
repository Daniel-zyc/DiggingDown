from Constant import *
import queue


class Map:
	def __init__(self, n = MAP_N, m = MAP_M, h = EMPTY_LAYER_H):
		self.n, self.m = n, m
		# logging.debug(f'map.n, m: {self.n, self.m}')

		self.ground_level = SCR_CEN_R
		self.road_level = self.ground_level + 1
		# logging.debug(f'map.ground_level: {self.ground_level}')
		# logging.debug(f'map.road_level: {self.road_level}')

		self.dirt_U = self.road_level + 1
		self.dirt_D = self.n
		self.dirt_L = 1
		self.dirt_R = self.m
		self.dirt_N = self.dirt_D - self.dirt_U + 1
		self.dirt_M = self.dirt_R - self.dirt_L + 1
		# logging.debug(f'map.dirt_UDLR: {self.dirt_U, self.dirt_D, self.dirt_L, self.dirt_R}')
		# logging.debug(f'map.dirt_H: {self.dirt_N}')

		self.reborn_R = self.ground_level
		self.reborn_C = self.m // 2 + 1
		# logging.debug(f'map.reborn_RC: {self.reborn_R, self.reborn_C}')

		self.layer = [self.road_level + h]
		for i in range(0, ORES_TOT):
			self.layer.append(self.layer[0]+(self.dirt_N-h)*(i+1)//ORES_TOT)
		# logging.debug(f'map.layer: {self.layer}')

		self.ores = self.ores_data = self.ores_tot = self.mp = None

	def in_dirt(self, r, c):
		return self.dirt_U <= r <= self.dirt_D and self.dirt_L <= c <= self.dirt_R

	def in_bound(self, r, c):
		return self.in_dirt(r, c) or r == self.ground_level or (r == self.road_level and c == self.reborn_C)

	def loc_to_reborn(self, r, c):
		r += (SCR_CEN_R - self.reborn_R)
		c += (SCR_CEN_C - self.reborn_C)
		return r, c

	def init_old(self, log_id):
		pass

	def init_new(self, sz_k = ORES_SIZE_K, num_k = ORES_NUM_K, layer_k = ORES_LAYER_K, grow_k = ORES_GROW_K, min_sz_k = ORES_MIN_SZ_K):
		self.ores = ORES.copy()
		self.ores_tot = ORES_TOT
		self.ores_data = ORES_DATA.copy()

		for i in range(0, self.ores_tot):
			ore = self.ores[i]
			self.ores_data[ore]['sz'] *= ORES_K[sz_k[i]]
			self.ores_data[ore]['num'] *= ORES_K[num_k[i]] * self.dirt_N * self.dirt_M // DENSITY_SIZE
			self.ores_data[ore]['layer'] *= ORES_K[layer_k[i]]
			self.ores_data[ore]['grow'] *= ORES_K[grow_k[i]]
			self.ores_data[ore]['min_sz'] *= ORES_K[min_sz_k[i]] * self.ores_data[ore]['sz'] // 10

		for i in range(0, self.ores_tot):
			ore = self.ores[i]
			end = min(i + self.ores_data[ore]['layer'], len(self.layer)-1)
			self.ores_data[ore]['range'] = [self.layer[i]+1, self.layer[end]]

		# logging.debug(f'map.ores_data: {self.ores_data}')

		self.__generate_map()

		# logging.debug(f'map.mp: {self.mp}')

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
				if rnd > self.ores_data[ore]['grow']:
					continue
				Q.put([nr, nc])
				self.mp[nr][nc] = ore
				sz -= 1
				if sz == 0:
					break

	def __generate_ore(self, ore):
		sz = random.randint(self.ores_data[ore]['min_sz'], self.ores_data[ore]['sz'])
		row = random.randint(self.ores_data[ore]['range'][0], self.ores_data[ore]['range'][1])
		col = random.randint(self.dirt_L, self.dirt_R)
		self.__grow_ore(ore, sz, row, col)

	def __generate_map(self):
		self.mp = [[DIRT] * (self.m + 1) for i in range(0, self.n + 1)]
		for i in range(0, self.ground_level + 1):
			self.mp[i] = [SKY] * (self.m + 1)
		self.mp[self.road_level] = [ROAD] * (self.m + 1)
		self.mp[self.road_level][self.reborn_C] = DIRT
		for ore in self.ores:
			for i in range(0, self.ores_data[ore]['num']):
				self.__generate_ore(ore)

