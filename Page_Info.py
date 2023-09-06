from Constant import *
from Menu import Background, MenuText
from Control import Control
from SpriteGroup import SpriteGroup
from Page import Page


class Page_Info(Page):
	def __init__(self):
		super().__init__()
		self.update_range = pg.Rect(0, 0, SCR_W, SCR_H)
		spg = SpriteGroup()
		self.list.append(Background())
		spg.add(MenuText('游戏信息', 64, posy = 0.15))
		self.esc = MenuText('返回 [ESC]', 36, color = LIGHT_RED, posy = 0.9)
		spg.add(self.esc)
		spg.add(MenuText('游戏开发人员：Daniel-zyc Mouxy Yooo_fan', 24, color = LIGHT_GREEN, posy = 0.35))
		spg.add(MenuText('游戏灵感来自一款 4399 上的小游戏，素材源自泰拉瑞亚', 24, posy = 0.45))
		spg.add(MenuText('游戏开发环境', 30, posy = 0.55))
		spg.add(MenuText('python 版本: 3.11.4  pygame 版本: 2.5.1', 24, posy = 0.65))
		spg.add(MenuText('PIL 版本: 10.0.0  imageio 版本: 2.31.2', 24, posy = 0.75))
		self.list.append(spg)

	def refresh(self, ctrl: Control):
		if ctrl.get_key(CTRL_ESC) or ctrl.get_click(self.esc.rect):
			return PAGE_EXIT
		return PAGE_NONE

