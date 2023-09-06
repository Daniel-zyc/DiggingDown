from Constant import *
from Menu import Block, MenuText
from Control import Control
from Page import Page
from SpriteGroup import SpriteGroup


class Page_WN(Page):
	def __init__(self, string: str = '请确认', title_sz: int = 30, opt_sz: int = 24, color = DARK_RED):
		super().__init__()
		spg = SpriteGroup()
		self.bg = Block(color = color)
		spg.add(self.bg)
		self.update_range = pg.Rect(self.bg.rect.x, self.bg.rect.y, self.bg.rect.w, self.bg.rect.h)
		spg.add(MenuText(string, title_sz, posy = 0.45))
		self.yes = MenuText('确认 [Enter]', opt_sz, posy = 0.55)
		spg.add(self.yes)
		self.list.append(spg)

	def refresh(self, ctrl: Control):
		if ctrl.get_key(CTRL_ENTER) or ctrl.get_click(self.yes.rect):
			return PAGE_EXIT
		return PAGE_NONE, None
