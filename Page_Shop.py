from Constant import *
from Control import Control
from PageEasy import PageEasy
from SpriteEasy import SpriteEasy
from Drill import Drill


class Page_Shop(PageEasy):
	def __init__(self, dr: Drill):
		super().__init__(SpriteEasy(PAGE_URL[P_SHOP]))
		self.dr = dr

	def refresh(self, ctrl: Control):
		if ctrl.get_key(CTRL_ESC) != CTRL_NONE:
			return PAGE_EXIT
		if ctrl.get_key(CTRL_OPT[1]) != CTRL_NONE:
			if self.dr.rgd_l < DRILL_LEVEL_MAX and self.dr.money >= DRILL_COST['rgd'][self.dr.rgd_l]:
				self.dr.money -= DRILL_COST['rgd'][self.dr.rgd_l]
				self.dr.rgd_l += 1
		if ctrl.get_key(CTRL_OPT[2]) != CTRL_NONE:
			if self.dr.eng_l < DRILL_LEVEL_MAX and self.dr.money >= DRILL_COST['eng'][self.dr.eng_l]:
				self.dr.money -= DRILL_COST['eng'][self.dr.eng_l]
				self.dr.eng_l += 1
		if ctrl.get_key(CTRL_OPT[3]) != CTRL_NONE:
			if self.dr.p_cap_l < DRILL_LEVEL_MAX and self.dr.money >= DRILL_COST['p_cap'][self.dr.p_cap_l]:
				self.dr.money -= DRILL_COST['p_cap'][self.dr.p_cap_l]
				self.dr.p_cap_l += 1
				self.dr.p_cap = DRILL_DATA['p_cap'][self.dr.p_cap_l]
		if ctrl.get_key(CTRL_OPT[4]) != CTRL_NONE:
			if self.dr.g_cap_l < DRILL_LEVEL_MAX and self.dr.money >= DRILL_COST['g_cap'][self.dr.g_cap_l]:
				self.dr.money -= DRILL_COST['g_cap'][self.dr.g_cap_l]
				self.dr.g_cap_l += 1
				self.dr.g_cap = DRILL_DATA['g_cap'][self.dr.g_cap_l]
		if ctrl.get_key(CTRL_OPT[5]) != CTRL_NONE:
			if self.dr.o_cap_l < DRILL_LEVEL_MAX and self.dr.money >= DRILL_COST['o_cap'][self.dr.o_cap_l]:
				self.dr.money -= DRILL_COST['o_cap'][self.dr.o_cap_l]
				self.dr.o_cap_l += 1
				self.dr.o_cap = DRILL_DATA['o_cap'][self.dr.o_cap_l]
		return PAGE_NONE
