from Constant import *
from Menu import Background, MenuText
from Control import Control
from Page import Page
from SpriteGroup import SpriteGroup
from Page_Achieve import Page_Achieve
from Page_Save import Page_Save
from Page_Key import Page_Key
from Page_Info import Page_Info
import Global as glb


class Page_Pause(Page):
	def __init__(self, mp, dr):
		super().__init__()
		self.update_range = pg.Rect(0, 0, SCR_W, SCR_H)
		self.mp, self.dr = mp, dr
		spg = SpriteGroup()
		self.list.append(Background())
		spg.add(MenuText('游戏暂停', 48, posy = 0.15))
		self.esc = MenuText('返回游戏 [ESC]', 36, color = LIGHT_GREEN, posy = 0.30)
		spg.add(self.esc)
		self.opt = [None]
		self.opt.append(MenuText('保存游戏 [1]', 36, posy = 0.45))
		self.opt.append(MenuText('查看按键 [2]', 36, posy = 0.55))
		self.opt.append(MenuText('查看档案 [3]', 36, posy = 0.65))
		self.opt.append(MenuText('游戏信息 [4]', 36, posy = 0.75))
		self.opt.append(MenuText('退出游戏 [5]', 36, color = LIGHT_RED, posy = 0.9))
		for i in range(1, len(self.opt)):
			spg.add(self.opt[i])
		self.list.append(spg)

	def refresh(self, ctrl: Control):
		if ctrl.get_key(CTRL_ESC) or ctrl.get_click(self.esc.rect):
			return PAGE_EXIT
		if ctrl.get_key(CTRL_OPT[1]) or ctrl.get_click(self.opt[1].rect):
			glb.pages.append(Page_Save(self.mp, self.dr))
		elif ctrl.get_key(CTRL_OPT[2]) or ctrl.get_click(self.opt[2].rect):
			glb.pages.append(Page_Key())
		elif ctrl.get_key(CTRL_OPT[3]) or ctrl.get_click(self.opt[3].rect):
			glb.pages.append(Page_Achieve())
		elif ctrl.get_key(CTRL_OPT[4]) or ctrl.get_click(self.opt[4].rect):
			glb.pages.append(Page_Info())
		elif ctrl.get_key(CTRL_OPT[5]) or ctrl.get_click(self.opt[5].rect):
			glb.pages.pop(-2)
			return PAGE_EXIT
		return PAGE_NONE
