from Constant import *
from Menu import Background, MenuText
from Control import Control
from SpriteGroup import SpriteGroup
from Page_Game import init_game
from Page import Page
import Global as glb


class Page_Read(Page):
	def __init__(self):
		super().__init__()
		self.update_range = pg.Rect(0, 0, SCR_W, SCR_H)
		spg = SpriteGroup()
		self.list.append(Background())
		spg.add(MenuText('读取存档', 64, posy = 0.15))
		self.esc = MenuText('返回 [ESC]', 36, color = LIGHT_RED, posy = 0.9)
		spg.add(self.esc)
		self.opt = [None]
		hf = LOG_NUM_MAX // 2
		for i in range(1, hf + 1):
			content = f'存档{i} [{i % 10}]: ' + glb.log.logs_info[i]
			self.opt.append(MenuText(content, 24, posx = 0.25, posy = 0.25 + i * 0.1))
			spg.add(self.opt[i])
		for i in range(hf + 1, LOG_NUM_MAX + 1):
			content = f'存档{i} [{i % 10}]: ' + glb.log.logs_info[i]
			self.opt.append(
				MenuText(content, 24, posx = 0.75, posy = 0.25 + (i - hf) * 0.1))
			spg.add(self.opt[i])
		self.list.append(spg)

	def refresh(self, ctrl: Control):
		if ctrl.get_key(CTRL_ESC) or ctrl.get_click(self.esc.rect):
			return PAGE_EXIT
		for i in range(1, LOG_NUM_MAX + 1):
			if not glb.log.logs[i]:
				continue
			if ctrl.get_key(CTRL_OPT[i]) or ctrl.get_click(self.opt[i].rect):
				glb.pages.pop()
				init_game()
				return PAGE_NONE
		return PAGE_NONE

