from Constant import *
from Menu import Background, MenuText
from Page import Page
from SpriteGroup import SpriteGroup
from Control import Control
import Global as glb


class Page_Achieve(Page):
	def __init__(self):
		super().__init__()
		self.update_range = pg.Rect(0, 0, SCR_W, SCR_H)
		self.data = glb.achieve.vals
		spg = SpriteGroup()
		self.list.append(Background())
		spg.add(MenuText('游戏档案', 64, posy = 0.1))
		self.esc = MenuText('返回 [ESC]', 36, color = LIGHT_RED, posy = 0.9)
		spg.add(self.esc)
		self.list.append(spg)
		self.prev = self.next = None
		self.text = SpriteGroup()
		self.idx = 0
		self.update()

	def refresh(self, ctrl: Control):
		if ctrl.get_key(CTRL_ESC) or ctrl.get_click(self.esc.rect):
			return PAGE_EXIT
		if self.prev is not None and (ctrl.get_key(CTRL_L) or ctrl.get_click(self.prev.rect)):
			self.idx -= 1
			self.update()
		elif self.next is not None and (ctrl.get_key(CTRL_R) or ctrl.get_click(self.next.rect)):
			self.idx += 1
			self.update()
		return PAGE_NONE

	def update(self):
		self.prev = self.next = None
		self.text.empty()
		if self.idx > 0:
			self.prev = MenuText('上一页 [A]', 36, posx = 0.2, posy = 0.9)
		if self.idx < 4:
			self.next = MenuText('下一页 [D]', 36, posx = 0.8, posy = 0.9)
		if self.idx == 0:
			self.text.add(MenuText(f'获得的金钱：{self.data["tot-money"]}', 30, posy = 0.25))
			self.text.add(MenuText(f'挖掘的土块：{self.data["tot-dirt"]}', 30, posy = 0.35))
			self.text.add(MenuText(f'挖掘的矿物：{self.data["tot-ore"]}', 30, posy = 0.45))
			self.text.add(MenuText(f'挖掘的宝箱：{self.data["tot-chest"]}', 30, posy = 0.55))
			self.text.add(MenuText(f'解救的 NPC：{self.data["tot-npc"]}', 30, posy = 0.65))
			self.text.add(MenuText(f'行走的距离：{self.data["tot-move"]}', 30, posy = 0.75))
		elif self.idx == 1:
			for i in range(0, DIRT_TOT):
				tmp = DIRTS[i]
				self.text.add(MenuText(f'挖掘的 {get_name(tmp)}：{self.data[tmp]}', 28, posy = 0.25 + i * 0.09))
		elif self.idx == 2:
			hf = ORE_TOT // 2 + 1
			for i in range(0, hf):
				tmp = ORES[i]
				self.text.add(MenuText(f'挖掘的 {get_name(tmp)}：{self.data[tmp]}', 20, posx = 0.25, posy = 0.22 + i * 0.058))
			for i in range(hf, ORE_TOT):
				tmp = ORES[i]
				self.text.add(MenuText(f'挖掘的 {get_name(tmp)}：{self.data[tmp]}', 20, posx = 0.75, posy = 0.22 + (i - hf) * 0.058))
		elif self.idx == 3:
			hf = CHEST_TOT // 2 + 1
			for i in range(0, hf):
				tmp = CHESTS[i]
				self.text.add(MenuText(f'获得的 {get_name(tmp)}：{self.data[tmp]}', 24, posx = 0.25, posy = 0.22 + i * 0.07))
			for i in range(hf, CHEST_TOT):
				tmp = CHESTS[i]
				self.text.add(MenuText(f'获得的 {get_name(tmp)}：{self.data[tmp]}', 24, posx = 0.75, posy = 0.22 + (i - hf) * 0.07))
		elif self.idx == 4:
			hf = NPC_TOT // 2 + 1
			for i in range(0, hf):
				tmp = NPCS[i]
				self.text.add(MenuText(f'解救的 {get_name(tmp)}：{self.data[tmp]}', 20, posx = 0.25, posy = 0.22 + i * 0.053))
			for i in range(hf, NPC_TOT):
				tmp = NPCS[i]
				self.text.add(MenuText(f'解救的 {get_name(tmp)}：{self.data[tmp]}', 20, posx = 0.75, posy = 0.22 + (i - hf) * 0.053))

	def draw(self, scr):
		for obj in self.list:
			obj.draw(scr)
		self.text.draw(scr)
		if self.prev is not None:
			self.prev.draw(scr)
		if self.next is not None:
			self.next.draw(scr)
