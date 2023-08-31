from Constant import *
from Control import Control
from PageEasy import PageEasy
from SpriteEasy import SpriteEasy


class Page_YN(PageEasy):
	def __init__(self):
		super().__init__(SpriteEasy(PAGE_URL[P_YN]))

	def refresh(self, ctrl: Control):
		key = ctrl.get_key(CTRL_ESC, CTRL_ENTER)
		if key == CTRL_NONE:
			return PAGE_NONE, None
		return PAGE_EXIT, key == CTRL_ENTER
