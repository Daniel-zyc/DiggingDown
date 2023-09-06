from Constant import *
from Menu import Background, MenuText
from Control import Control
from SpriteGroup import SpriteGroup
from Page import Page


class Page_Key(Page):
	def __init__(self):
		super().__init__()
		self.update_range = pg.Rect(0, 0, SCR_W, SCR_H)
		spg = SpriteGroup()
		self.list.append(Background())
		spg.add(MenuText('游戏按键', 64, posy = 0.15))
		self.esc = MenuText('返回 [ESC]', 36, color = LIGHT_RED, posy = 0.9)
		spg.add(self.esc)
		spg.add(MenuText('取消&暂停 [ESC]', 24, color = LIGHT_RED, posx = 0.375, posy = 0.30))
		spg.add(MenuText('确认 [Enter, Space]', 24, color = LIGHT_GREEN, posx = 0.625, posy = 0.30))
		spg.add(MenuText('上 [W, ↑]  下 [S, ↓]  左 [A, ←]  右[D, →]', 24, posy = 0.38))
		spg.add(MenuText('加速 [Left Shift, Right Shift] ', 24, posy = 0.46))
		spg.add(MenuText('与商店互动（需要在商店前） [Space]', 24, posy = 0.54))
		spg.add(MenuText('开关 NPC 列表 [E]  开关携带矿物列表 [F]', 24, posy = 0.62))
		spg.add(MenuText('查看游戏档案 [R]  查看游戏按键 [G]', 24, posy = 0.70))
		spg.add(MenuText('切换游戏运行详细信息 [Tab]', 24, posy = 0.78))
		self.list.append(spg)

	def refresh(self, ctrl: Control):
		if ctrl.get_key(CTRL_ESC) or ctrl.get_click(self.esc.rect):
			return PAGE_EXIT
		return PAGE_NONE

