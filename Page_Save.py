from Constant import *
from Control import Control
from PageEasy import PageEasy
from SpriteEasy import SpriteEasy
import Global as glb


class Page_Save(PageEasy):
	def __init__(self):
		super().__init__(SpriteEasy(PAGE_URL[P_SAVE]))

	def refresh(self, ctrl: Control):
		if ctrl.get_key(CTRL_ESC) != CTRL_NONE:
			return PAGE_EXIT
		key = ctrl.get_key(*CTRL_OPT[1:])
		if key != CTRL_NONE:
			status = glb.get_YN()
			if status:
				pass
		return PAGE_NONE

