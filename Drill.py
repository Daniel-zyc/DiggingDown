from Constant import *


class Drill:
	def __init__(self):
		self.rgd_l = self.eng_l = self.h_l = self.p_l = self.g_l = self.o_l = 0
		self.h_max = self.o_max = self.p_max = self.g_max = 0
		self.money = 0
		self.h = self.o = self.p = self.g = 0
		self.r = self.c = 0
		self.carry = {}
		for ore in ORES:
			self.carry[ore] = 0

	def init_new(self, r, c):
		self.o_max = DRILL_DATA['o_max'][self.o_l]
		self.h = self.h_max = DRILL_DATA['h_max'][self.h_l]
		self.g = self.g_max = DRILL_DATA['g_max'][self.g_l]
		self.p = self.p_max = DRILL_DATA['p_max'][self.p_l]
		self.r, self.c = r, c

