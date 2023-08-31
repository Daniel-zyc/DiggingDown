from Constant import *
from Control import Control
from Page import Page
from Sprite_Menu import Sprite_Menu
from Page_Keys import Page_Keys
from Page_Info import Page_Info
from Page_Game import Page_Game
import Global as glb


class Page_Menu(Page):
	def __init__(self):
		super().__init__()
		sp = Sprite_Menu()
		self.update_range = PG.Rect(sp.rect.x, sp.rect.y, sp.rect.width, sp.rect.height)
		spg = PG.sprite.Group()
		spg.add(sp)
		self.spg_list.append(spg)

	def refresh(self, ctrl: Control):
		if ctrl.get_short_key(CTRL_ESC) != CTRL_NONE:
			return PAGE_EXIT
		if ctrl.get_short_key(CTRL_OPT[1]):
			glb.pages.append(Page_Game())
			return PAGE_NONE
		if ctrl.get_short_key(CTRL_OPT[4]):
			glb.pages.append(Page_Keys())
			return PAGE_NONE
		if ctrl.get_short_key(CTRL_OPT[5]):
			glb.pages.append(Page_Info())
			return PAGE_NONE
		return PAGE_NONE

