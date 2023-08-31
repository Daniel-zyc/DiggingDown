from Constant import *
from Control import Control
from PageEasy import PageEasy
from SpriteEasy import SpriteEasy
from Page_Game import Page_Game
import Global as glb
import ToolFunc as tool


class Page_Read(PageEasy):
	def __init__(self):
		super().__init__(SpriteEasy(PAGE_URL[P_READ]))

	def refresh(self, ctrl: Control):
		if ctrl.get_key(CTRL_ESC) != CTRL_NONE:
			return PAGE_EXIT
		for i in range(1, LOG_NUM_MAX+1):
			if not glb.log.logs[i]:
				continue
			if ctrl.get_key(CTRL_OPT[i]) != CTRL_NONE:
				glb.pages.append(Page_Game(i))
				tool.swap(glb.pages[-1], glb.pages[-2])
				return PAGE_EXIT
		return PAGE_NONE

