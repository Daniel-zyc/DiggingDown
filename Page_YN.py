from Constant import *
from Menu import MenuBlock, MenuText
from Control import Control
from Page import Page
from SpriteGroup import SpriteGroup


class Page_YN(Page):
	def __init__(self, string: str = '请确认', title_sz: int = 30, opt_sz: int = 24):
		super().__init__()
		spg = SpriteGroup()
		self.bg = MenuBlock()
		spg.add(self.bg)
		self.update_range = pg.Rect(self.bg.rect.x, self.bg.rect.y, self.bg.rect.w, self.bg.rect.h)
		spg.add(MenuText(string, title_sz, posy = 0.45))
		self.yes = MenuText('确认 [Enter]', opt_sz, posx = 0.375, posy = 0.55)
		self.no = MenuText('取消 [ESC]', opt_sz, posx = 0.625, posy = 0.55)
		spg.add(self.yes)
		spg.add(self.no)
		self.list.append(spg)

	def refresh(self, ctrl: Control):
		key = ctrl.get_key(CTRL_ESC, CTRL_ENTER)
		if key:
			return PAGE_EXIT, key == CTRL_ENTER
		if ctrl.get_click(self.yes.rect):
			return PAGE_EXIT, True
		if ctrl.get_click(self.no.rect):
			return PAGE_EXIT, False
		return PAGE_NONE, None
