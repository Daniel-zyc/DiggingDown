from Constant import *
from Control import Control
from Page import Page
from Sprite_Pause import Sprite_Pause
from Page_Keys import Page_Keys
import Global as glb


class Page_Pause(Page):
	def __init__(self):
		super().__init__()
		sp = Sprite_Pause()
		self.update_range = PG.Rect(sp.rect.x, sp.rect.y, sp.rect.width, sp.rect.height)
		spg = PG.sprite.Group()
		spg.add(sp)
		self.spg_list.append(spg)

	def refresh(self, ctrl: Control):
		key = ctrl.get_short_key(CTRL_ESC, CTRL_ENTER)
		if key != CTRL_NONE:
			return PAGE_EXIT
		if ctrl.get_short_key(CTRL_OPT[3]):
			glb.pages.append(Page_Keys())
			return PAGE_NONE
		if ctrl.get_short_key(CTRL_OPT[4]):
			glb.pages.pop(-2)
			return PAGE_EXIT

		return PAGE_NONE

