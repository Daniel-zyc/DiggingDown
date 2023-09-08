from Constant import *
from Control import Control
from Page import Page
from SpriteGroup import SpriteGroup
from Sprite import Sprite


class PageEasy(Page):
	def __init__(self, sp: Sprite, range = None,*args):
		super().__init__()
		if range is None:
			self.update_range = pg.Rect(sp.rect.x, sp.rect.y, sp.rect.width, sp.rect.height)
		else:
			self.update_range = range
		spg = SpriteGroup()
		spg.add(sp)
		for arg in args:
			spg.add(arg)
		self.list.append(spg)

	def refresh(self, ctrl: Control):
		key = ctrl.get_key(CTRL_ESC, CTRL_ENTER)
		if key != CTRL_NONE:
			return PAGE_EXIT
		return PAGE_NONE
