from Constant import *
from Control import Control
from Page import Page
from Sprite_Achieve import Sprite_Achieve


class Page_Achieve(Page):
	def __init__(self):
		super().__init__()
		sp = Sprite_Achieve()
		self.update_range = PG.Rect(sp.rect.x, sp.rect.y, sp.rect.width, sp.rect.height)
		spg = PG.sprite.Group()
		spg.add(sp)
		self.spg_list.append(spg)

	def refresh(self, ctrl: Control):
		key = ctrl.get_short_key(CTRL_ESC, CTRL_ENTER)
		if key != CTRL_NONE:
			return PAGE_EXIT
		return PAGE_NONE