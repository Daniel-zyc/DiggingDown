from Constant import *
from Menu import Background, MenuText
from Control import Control
from Page import Page
import Global as glb


class Page_Save(Page):
	def __init__(self, mp, dr):
		super().__init__()
		self.mp, self.dr = mp, dr
		self.update_range = pg.Rect(0, 0, SCR_W, SCR_H)
		self.list.append(Background())
		self.list.append(MenuText('保存存档', 64, posy = 0.15))
		self.esc = MenuText('返回 [ESC]', 36, color = LIGHT_RED, posy = 0.9)
		self.list.append(self.esc)
		self.opt = None
		self.update()

	def save(self, idx):
		if glb.log.logs[idx]:
			status = glb.get_YN(f'请确认是否存入 {idx} 号存档，旧的存档将被覆盖')
			if status:
				glb.log.log_save(idx, self.mp, self.dr)
		else:
			glb.log.log_save(idx, self.mp, self.dr)

	def refresh(self, ctrl: Control):
		if ctrl.get_key(CTRL_ESC) or ctrl.get_click(self.esc.rect):
			return PAGE_EXIT
		key = ctrl.get_key(*CTRL_OPT[1:])
		if key != CTRL_NONE:
			self.save(key - CTRL_OPT[0])
			return PAGE_NONE
		for i in range(1, LOG_NUM_MAX + 1):
			if ctrl.get_click(self.opt[i].rect):
				self.save(i)
		self.update()
		return PAGE_NONE

	def draw(self, scr):
		for obj in self.list:
			obj.draw(scr)
		for i in range(1, len(self.opt)):
			self.opt[i].draw(scr)

	def update(self):
		self.opt = [None]
		hf = LOG_NUM_MAX // 2
		for i in range(1, hf + 1):
			content = f'存档{i} [{i % 10}]: ' + glb.log.logs_info[i]
			self.opt.append(
				MenuText(content, 24, posx = 0.25, posy = 0.25 + i * 0.1))
		for i in range(hf + 1, LOG_NUM_MAX + 1):
			content = f'存档{i} [{i % 10}]: ' + glb.log.logs_info[i]
			self.opt.append(
				MenuText(content, 24, posx = 0.75, posy = 0.25 + (i - hf) * 0.1))

