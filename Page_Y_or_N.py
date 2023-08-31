from Constant import *
from Control import Control
from Page import Page
from Sprite_Y_or_N import Sprite_Y_or_N


class Page_Y_or_N(Page):
	def __init__(self):
		super().__init__()
		sp = Sprite_Y_or_N()
		self.update_range = PG.Rect(sp.rect.x, sp.rect.y, sp.rect.width, sp.rect.height)
		spg = PG.sprite.Group()
		spg.add(sp)
		self.spg_list.append(spg)

	def refresh(self, ctrl: Control):
		key = ctrl.get_short_key(CTRL_ESC, CTRL_ENTER)
		if key == CTRL_NONE:
			return PAGE_NONE, None
		if key == CTRL_ESC:
			return PAGE_EXIT, False
		return PAGE_EXIT, True
