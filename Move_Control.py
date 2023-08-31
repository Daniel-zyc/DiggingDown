from Constant import *
from Map import Map
from SpriteGroup import SpriteGroup
import Global as glb


class Move_Control:
	def __init__(self, mp: Map):
		self.mp = mp
		self.is_moving = 0
		self.dir = D_N
		self.sp = SPEED_LEVEL[0][0]
		self.cur = self.sp[1]
		self.r = self.mp.reborn_R
		self.c = self.mp.reborn_C
		self.nr = self.nc = 0
		self.pixel = 0

	def try_move(self, d, speedup):
		if self.is_moving:
			return
		nr, nc = self.r + D_XY[d][0], self.c + D_XY[d][1]
		if not self.mp.in_bound(nr, nc):
			return
		self.sp = glb.get_speed_level(self.mp.mp[nr][nc], 0, speedup)
		if self.sp[0] == 0:
			return
		self.nr, self.nc = nr, nc
		self.dir = d
		self.is_moving = 1
		self.cur = self.sp[1]
		self.pixel = 0

	def move(self):
		ret_d, ret_sp = D_MP[self.dir], 0
		self.cur -= 1
		if self.cur == 0:
			self.pixel += self.sp[0]
			ret_sp = self.sp[0]
			self.cur = self.sp[1]
		if self.pixel == BLOCK_SZ:
			self.r, self.c = self.nr, self.nc
			self.pixel = 0
			self.is_moving = 0
			return ret_d, ret_sp, self.r, self.c
		return ret_d, ret_sp, 0, 0




