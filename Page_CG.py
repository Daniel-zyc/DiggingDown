from Constant import *
from Menu import MenuBackground, MenuText
from Control import Control
from Sprite import Sprite
from SpriteGroup import SpriteGroup
from Page import Page


class Page_CG(Page):
	def __init__(self):
		super().__init__()
		self.update_range = pg.Rect(0, 0, SCR_W, SCR_H)
		spg = SpriteGroup()
		self.idx = 0
		self.list.append(MenuBackground(CG_IMG_URL.format(self.idx), False))
		self.nxt = MenuText('继续 [Enter]', 36, posx = 0.85, posy = 0.9)
		mask = Sprite()
		mask.image = pg.surface.Surface((self.nxt.rect.w + 20, self.nxt.rect.h + 20))
		mask.image.set_alpha(144)
		mask.rect = mask.image.get_rect()
		mask.rect.center = self.nxt.rect.center
		spg.add(mask)
		spg.add(self.nxt)
		self.list.append(spg)

	def refresh(self, ctrl: Control):
		if ctrl.get_key(CTRL_ENTER) or ctrl.get_click(self.nxt.rect):
			self.idx += 1
			if self.idx >= CG_LEN:
				return PAGE_EXIT
			self.update()
		return PAGE_NONE

	def update(self):
		self.list[0] = MenuBackground(CG_IMG_URL.format(self.idx), False)


