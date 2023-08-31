from Constant import *
from Control import Control
from Page import Page
from SpriteGroup import SpriteGroup
from Sprite_Cover import Sprite_Cover
from Sprite_Cloud import Sprite_Cloud
from Sprite_Tree import Sprite_Tree
from Sprite_Block import Sprite_Block
from Move_Control import Move_Control
from Sprite_Drill import Sprite_Drill
from Page_Pause import Page_Pause
from Map import Map
import Global as glb


class Page_Game(Page):
	def __init__(self, log_id = 0):
		super().__init__()
		self.update_range = (0, 0, SCR_W, SCR_H)
		self.mp = Map()
		if log_id == 0:
			self.mp.init_new()
		else:
			self.mp.init_old(log_id)
		# logging.debug(f'Page_Game self.mp.n, m: {self.mp.n, self.mp.m}')

		self.bg_spg = SpriteGroup()
		self.init_background()
		self.spg_list.append(self.bg_spg)

		self.mp_sp = [[None] for i in range(0, self.mp.n+1)]
		self.mp_spg = SpriteGroup()
		self.init_map()

		self.spg_list.append(self.mp_spg)

		self.dr_spg = SpriteGroup()
		self.init_drill()
		self.spg_list.append(self.dr_spg)

		self.mv = Move_Control(self.mp)

	def refresh(self, ctrl: Control):
		key = ctrl.get_short_key(CTRL_ESC)
		if key != CTRL_NONE:
			glb.pages.append(Page_Pause())
			return PAGE_NONE
		if not self.mv.is_moving:
			key = ctrl.get_long_key(CTRL_D, CTRL_L, CTRL_R, CTRL_U)
			if key != CTRL_NONE:
				speedup = ctrl.get_long_key(CTRL_SH) != CTRL_NONE
				self.mv.try_move(CTRL_DIR[key], speedup)
		if self.mv.is_moving:
			d, sp, r, c = self.mv.move()
			self.bg_spg.move(d, sp)
			self.mp_spg.move(d, sp)
			if r != 0 and c != 0:
				self.dr_cover_blk(r, c)

		self.update()
		return PAGE_NONE

	def init_background(self):
		r, c = self.mp.loc_to_reborn(1, 1)
		x, y = glb.b_to_p_tl(r, c)
		self.bg_spg.add(Sprite_Cover(SKY, x, y))

		cloud_cnt = CLOUD_NUM * self.mp.m * self.mp.ground_level // CLOUD_DENSITY_SIZE
		# logging.debug(f'Page_Game.cloud_cnt: {cloud_cnt}')
		for i in range(0, cloud_cnt):
			r = random.randint(1, self.mp.ground_level//2)
			c = random.randint(1, self.mp.m)
			r, c = self.mp.loc_to_reborn(r, c)
			x, y = glb.b_to_p_tl(r, c)
			# logging.debug(f'cloud pos: {x, y}')
			self.bg_spg.add(Sprite_Cloud(CLOUDS[0], x, y))

		tree_cnt = TREE_NUM * self.mp.m // TREE_DENSITY_SIZE
		# logging.debug(f'Page_Game.tree_cnt: {tree_cnt}')
		for i in range(0, tree_cnt):
			r = self.mp.road_level
			c = random.randint(1, self.mp.m)
			r, c = self.mp.loc_to_reborn(r, c)
			x, y = glb.b_to_p_tl(r, c)
			self.bg_spg.add(Sprite_Tree(TREES[0], x, y))

		r, c = self.mp.loc_to_reborn(self.mp.road_level, self.mp.dirt_L)
		x, y = glb.b_to_p_tl(r, c)
		self.bg_spg.add(Sprite_Cover(EMPTY_BG, x, y))

		r, c = self.mp.loc_to_reborn(1, self.mp.m+1)
		x, y = glb.b_to_p_tl(r, c)
		self.bg_spg.add(Sprite_Cover(COVER, x, y))

		r, c = self.mp.loc_to_reborn(self.mp.n+1, 1)
		x, y = glb.b_to_p_tl(r, c)
		self.bg_spg.add(Sprite_Cover(COVER, x, y))

	def init_map(self):
		# logging.debug(f'init_map: {self.mp_sp}')
		for i in range(self.mp.road_level, self.mp.n + 1):
			for j in range(1, self.mp.m+1):
				r, c = self.mp.loc_to_reborn(i, j)
				x, y = glb.b_to_p_tl(r, c)
				# logging.debug(f'Page_Game.init_map: {i, j}')
				# logging.debug(f'Page_Game.init_map: {i, j, self.mp.mp[i][j]}')
				self.mp_sp[i].append(Sprite_Block(self.mp.mp[i][j], x, y))
				self.mp_spg.add(self.mp_sp[i][-1])

	def init_drill(self):
		r, c = self.mp.reborn_R, self.mp.reborn_C
		r, c = self.mp.loc_to_reborn(r, c)
		x, y = glb.b_to_p_tl(r, c)
		self.dr_spg.add(Sprite_Drill(D_BODYS[0], x, y))

	def update(self):
		self.bg_spg.update()
		self.dr_spg.update()

	def dr_cover_blk(self, r, c):
		if r <= self.mp.ground_level:
			return
		if self.mp.mp[r][c] != EMPTY:
			self.mp_sp[r][c].kill()
			self.mp.mp[r][c] = EMPTY
