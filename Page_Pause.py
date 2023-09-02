from Constant import *
from Control import Control
from PageEasy import PageEasy
from SpriteEasy import SpriteEasy
from Page_Achieve import Page_Achieve
from Page_Save import Page_Save
import Global as glb


class Page_Pause(PageEasy):
	def __init__(self, mp, dr):
		super().__init__(SpriteEasy(PAGE_URL[P_PAUSE]))
		self.mp = mp
		self.dr = dr

	def refresh(self, ctrl: Control):
		if ctrl.get_key(CTRL_ESC) != CTRL_NONE:
			return PAGE_EXIT
		if ctrl.get_key(CTRL_OPT[1]) != CTRL_NONE:
			glb.pages.append(Page_Save(self.mp, self.dr))
		elif ctrl.get_key(CTRL_OPT[2]) != CTRL_NONE:
			glb.pages.append(PageEasy(SpriteEasy(PAGE_URL[P_KEYS])))
		elif ctrl.get_key(CTRL_OPT[3]) != CTRL_NONE:
			glb.pages.append(Page_Achieve())
		elif ctrl.get_key(CTRL_OPT[4]) != CTRL_NONE:
			glb.pages.append(PageEasy(SpriteEasy(PAGE_URL[P_INFO])))
		elif ctrl.get_key(CTRL_OPT[5]) != CTRL_NONE:
			glb.pages.pop(-2)
			return PAGE_EXIT
		return PAGE_NONE
