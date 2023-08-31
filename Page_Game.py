from Constant import *
from Control import *
from PageEasy import PageEasy
from SpriteEasy import SpriteEasy
from Page_Pause import Page_Pause
import Global as glb


class Page_Game(PageEasy):
	def __init__(self, log_id = 0):
		super().__init__(SpriteEasy('./assets/img/page/game.png'))

	def refresh(self, ctrl: Control):
		if ctrl.get_key(CTRL_ESC) != CTRL_NONE:
			glb.pages.append(Page_Pause())
		return PAGE_NONE
