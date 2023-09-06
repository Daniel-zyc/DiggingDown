from Constant import *
from Control import Control
from Page import Page
from SpriteGroup import SpriteGroup
from Sprite import Sprite


class PageEasy(Page):
	def __init__(self, sp: Sprite, *args):
		super().__init__()
		self.update_range = pg.Rect(sp.rect.x, sp.rect.y, sp.rect.width, sp.rect.height)
		spg = SpriteGroup()
		spg.add(sp)
		for arg in args:
			spg.add(arg)
		self.list.append(spg)

	def refresh(self, ctrl: Control):
		key = ctrl.get_key(CTRL_ESC)
		if key != CTRL_NONE:
			return PAGE_EXIT
		return PAGE_NONE
