from Constant import *
from Control import Control
from PageEasy import PageEasy
from SpriteEasy import SpriteEasy
from Page_Achieve import Page_Achieve
from Page_Read import Page_Read
from Page_Game import Page_Game
import Global as glb


class Page_Menu(PageEasy):
	def __init__(self):
		super().__init__(SpriteEasy(PAGE_URL[P_MENU]))
		self.update_range = pg.Rect(0, 0, SCR_W, SCR_H)

	def refresh(self, ctrl: Control):
		if ctrl.get_key(CTRL_ESC) != CTRL_NONE:
			return PAGE_EXIT
		if ctrl.get_key(CTRL_OPT[1]) != CTRL_NONE:
			glb.pages.append(Page_Game())
		elif ctrl.get_key(CTRL_OPT[2]) != CTRL_NONE:
			glb.pages.append(Page_Read())
		elif ctrl.get_key(CTRL_OPT[3]) != CTRL_NONE:
			glb.pages.append(Page_Achieve())
		elif ctrl.get_key(CTRL_OPT[4]) != CTRL_NONE:
			glb.pages.append(PageEasy(SpriteEasy(PAGE_URL[P_KEYS])))
		elif ctrl.get_key(CTRL_OPT[5] != CTRL_NONE):
			glb.pages.append(PageEasy(SpriteEasy(PAGE_URL[P_INFO])))
		return PAGE_NONE
