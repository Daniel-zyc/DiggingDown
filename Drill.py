from Constant import *


class Drill:
	def __init__(self):
		self.rgd_l = self.eng_l = self.p_cap_l = self.g_cap_l = self.o_cap_l = 0
		self.money = self.carry = 0
		self.o_cur = self.p_cur = self.g_cur = 0
		self.r = self.c = 0
		self.o_cap = self.p_cap = self.g_cap = 0

	def init_new(self, r, c):
		self.p_cur = self.p_cap = DRILL_DATA['p_cap'][self.p_cap_l]
		self.g_cur = self.g_cap = DRILL_DATA['g_cap'][self.g_cap_l]
		self.o_cap = DRILL_DATA['o_cap'][self.o_cap_l]
		self.r, self.c = r, c

