from Constant import *
from Control import *
from Page import Page
from Map import Map
from Drill import Drill
from PageEasy import PageEasy
from Page_Pause import Page_Pause
from Page_Shop import Page_Shop
from SpriteGroup import SpriteGroup
from SpriteEasy import SpriteEasy
from Sprite_Cloud import Sprite_Cloud
from SpriteMulti import SpriteMulti
from Text import Text
from datetime import datetime
import ToolFunc as tool
import Global as glb


class Page_Game(Page):
	def __init__(self, log_id = 0):
		super().__init__()
		self.update_range = pg.Rect(0, 0, SCR_W, SCR_H)
		self.mp = Map()
		self.dr = Drill()
		if log_id != 0:
			glb.log.log_read(log_id, self.mp, self.dr)
			self.r, self.c = self.dr.r, self.dr.c
		else:
			self.mp.init_new()
			self.r, self.c = self.mp.reborn_R, self.mp.reborn_C
			self.dr.init_new(self.r, self.c)
		self.rgd = self.dr.rgd_l
		self.eng = self.dr.eng_l
		self.g_cap = self.dr.g_cap_l
		self.cloud_num = self.cloud_num_max = CLOUD_NUM_MAX * self.mp.m * self.mp.g_level // CLOUD_DENSITY_SIZE
		self.tree_num = self.tree_num_max = TREE_NUM_MAX*self.mp.m // TREE_DENSITY_LEN
		self.sky = None
		self.sky_spg = SpriteGroup()
		self.cld_spg = SpriteGroup()
		self.bg_spg = SpriteGroup()
		self.mp_sp = [[None] for i in range(0, self.mp.n + 1)]
		self.mp_spg = SpriteGroup()
		self.dr_h = self.dr_b = self.dr_f = None
		self.dr_spg = SpriteGroup()
		self.info = Text()
		self.init_bg()
		self.init_mp()
		self.init_dr()
		self.show_info = 0
		self.list = [self.sky_spg, self.cld_spg, self.bg_spg, self.mp_spg, self.dr_spg]
		self.is_moving = 0
		self.dir = D_R
		self.speed = SPEED_LEVEL[0][0]
		self.speedup = 0
		self.pixel = 0
		self.nr, self.nc = 0, 0
		self.mv_timer = self.speed[1]
		self.upgrade = 0
		self.pre_time = datetime.now()
		self.over = 0

	def init_bg(self):
		x, y = tool.loc_b_to_p(1, 1, self.r, self.c)
		self.sky = SpriteEasy(BG_IMG_URL[SKY], x, y)
		self.sky_spg.add(self.sky)

		self.cloud_num = random.randint(1, self.cloud_num_max)
		for i in range(0, self.cloud_num):
			r = random.randint(1, self.mp.g_level//2)
			c = random.randint(1, self.mp.m)
			x, y = tool.loc_b_to_p(r, c, self.r, self.c)
			self.cld_spg.add(self.generate_cloud(x, y))

		self.tree_num = random.randint(1, self.tree_num_max)
		for i in range(0, self.tree_num):
			self.bg_spg.add(self.generate_tree())

		x, y = tool.loc_b_to_p(self.mp.reborn_R - SHOP_N[PETROL_SHOP] + 1, self.mp.reborn_C + SHOP_POS[PETROL_SHOP], self.r, self.c)
		self.bg_spg.add(SpriteMulti(BG_IMG_URL[PETROL_SHOP], x, y))

		x, y = tool.loc_b_to_p(self.mp.reborn_R - SHOP_N[GAS_SHOP] + 1, self.mp.reborn_C + SHOP_POS[GAS_SHOP], self.r, self.c)
		self.bg_spg.add(SpriteMulti(BG_IMG_URL[GAS_SHOP], x, y))

		x, y = tool.loc_b_to_p(self.mp.reborn_R - SHOP_N[ORES_SHOP] + 1, self.mp.reborn_C + SHOP_POS[ORES_SHOP], self.r, self.c)
		self.bg_spg.add(SpriteMulti(BG_IMG_URL[ORES_SHOP], x, y))

		x, y = tool.loc_b_to_p(self.mp.reborn_R - SHOP_N[DRILL_SHOP] + 1, self.mp.reborn_C + SHOP_POS[DRILL_SHOP], self.r, self.c)
		self.bg_spg.add(SpriteMulti(BG_IMG_URL[DRILL_SHOP], x, y))

		x, y = tool.loc_b_to_p(self.mp.n, 1, self.r, self.c)
		tmp = SpriteEasy(BG_IMG_URL[COVER], x, y)
		tmp.rect.bottomright = (x, y)
		self.bg_spg.add(tmp)

		x, y = tool.loc_b_to_p(self.mp.r_level, 1, self.r, self.c)
		self.bg_spg.add(SpriteEasy(BG_IMG_URL[EMPTY_BG], x, y))

		x, y = tool.loc_b_to_p(1, self.mp.m + 1, self.r, self.c)
		self.bg_spg.add(SpriteEasy(BG_IMG_URL[COVER], x, y))

		x, y = tool.loc_b_to_p(self.mp.n + 1, 1, self.r, self.c)
		self.bg_spg.add(SpriteEasy(BG_IMG_URL[COVER], x, y))

	def generate_cloud(self, x = None, y = None):
		d = random.randint(0, 1)
		sp = random.randint(0, 9)
		idx = random.randint(0, CLOUD_LEN - 1)
		if y is None:
			y = random.randint(self.sky.rect.y, self.sky.rect.y + self.mp.g_level*BLOCK_SZ//2)
			if d == 0:
				x = self.sky.rect.x
			else:
				x = self.sky.rect.x + self.mp.m * BLOCK_SZ
		return Sprite_Cloud(idx, d, CLOUD_SP[sp], x, y)

	def generate_tree(self):
		r, c = self.mp.r_level, random.randint(1, self.mp.m)
		x, y = tool.loc_b_to_p(r, c, self.r, self.c)
		idx = random.randint(0, TREE_LEN-1)
		tmp = SpriteMulti(BG_IMG_URL[TREE], x, y, idx)
		tmp.rect.left = x
		tmp.rect.bottom = y
		return tmp

	def init_mp(self):
		for i in range(self.mp.r_level, self.mp.n + 1):
			for j in range(1, self.mp.m + 1):
				if self.mp.mp[i][j] == EMPTY:
					self.mp_sp[i].append(None)
					continue
				x, y = tool.loc_b_to_p(i, j, self.r, self.c)
				self.mp_sp[i].append(SpriteEasy(BLK_IMG_URL[self.mp.mp[i][j]], x, y))
				self.mp_spg.add(self.mp_sp[i][-1])

	def init_dr(self):
		self.dr_h = self.get_drill_sp(HEAD, self.dr.rgd_l)
		self.dr_b = self.get_drill_sp(BODY, self.dr.eng_l)
		self.dr_f = [self.get_drill_sp(SFLAME, self.dr.g_cap_l), self.get_drill_sp(LFLAME, self.dr.g_cap_l)]
		self.dr_spg.add(self.dr_h[D_R])
		self.dr_spg.add(self.dr_b[D_R])
		self.dr_spg.add(self.dr_f[0][D_R])

	def check_upgrade(self):
		if self.rgd == self.dr.rgd_l and self.eng == self.dr.eng_l and self.g_cap == self.dr.g_cap_l:
			return
		self.dr_spg.empty()
		if self.rgd != self.dr.rgd_l:
			self.dr_h = self.get_drill_sp(HEAD, self.dr.rgd_l)
			self.rgd = self.dr.rgd_l
		if self.eng != self.dr.eng_l:
			self.dr_b = self.get_drill_sp(BODY, self.dr.eng_l)
			self.eng = self.dr.eng_l
		if self.g_cap != self.dr.g_cap_l:
			self.dr_f = [self.get_drill_sp(SFLAME, self.dr.g_cap_l), self.get_drill_sp(LFLAME, self.dr.g_cap_l)]
		self.dr_spg.add(self.dr_h[self.dir])
		self.dr_spg.add(self.dr_b[self.dir])
		self.dr_spg.add(self.dr_f[self.speedup][self.dir])

	def get_drill_sp(self, part, level):
		ret = [None]
		xx = [SCR_CEN_R, SCR_CEN_R, SCR_CEN_R, SCR_CEN_R, SCR_CEN_R]
		yy = [SCR_CEN_C, SCR_CEN_C, SCR_CEN_C, SCR_CEN_C, SCR_CEN_C]
		if part == HEAD:
			for d in range(1, 5):
				xx[d], yy[d] = xx[d] + D_XY[d][0], yy[d] + D_XY[d][1]
		elif part == SFLAME or part == LFLAME:
			for d in range(1, 5):
				xx[d], yy[d] = xx[d] - D_XY[d][0], yy[d] - D_XY[d][1]
		for d in range(1, 5):
			xx[d], yy[d] = tool.b_to_p_tl(xx[d], yy[d])
		ret.append(SpriteMulti(DR_IMG_URL[part], xx[1], yy[1], 1, level))
		ret[-1].set_colorkey((255, 255, 255))
		ret.append(SpriteMulti(DR_IMG_URL[part], xx[2], yy[2], 2, level))
		ret[-1].set_colorkey((255, 255, 255))
		ret.append(SpriteMulti(DR_IMG_URL[part], xx[3], yy[3], 1, level))
		ret[-1].flip_images()
		ret[-1].set_colorkey((255, 255, 255))
		ret.append(SpriteMulti(DR_IMG_URL[part], xx[4], yy[4], 2, level))
		ret[-1].flip_images(False, True)
		ret[-1].set_colorkey((255, 255, 255))
		return ret

	def refresh(self, ctrl: Control):
		if self.upgrade:
			self.check_upgrade()
		self.upgrade = 0
		if not self.over and self.dr.p_cur == 0 and (self.dr.money == 0 or not self.mp.in_shop(PETROL_SHOP, self.r, self.c)):
			self.over = 1
			glb.pages.append(PageEasy(SpriteEasy(PAGE_URL[P_OVER])))
		if ctrl.get_key(CTRL_ESC) != CTRL_NONE:
			self.dr.r, self.dr.c = self.r, self.c
			glb.pages.append(Page_Pause(self.mp, self.dr))
		if ctrl.get_key(CTRL_TAB) != CTRL_NONE:
			self.switch_info()
		if not self.is_moving:
			if ctrl.get_press(CTRL_U, CTRL_D, CTRL_L, CTRL_R) != CTRL_NONE:
				d = CTRL_DIR[ctrl.get_press(CTRL_U, CTRL_D, CTRL_L, CTRL_R)]
				self.try_move(d, ctrl.get_press(CTRL_SH) != CTRL_NONE)
		else:
			self.move()
		if not self.is_moving and ctrl.get_key(CTRL_INTER) != CTRL_NONE:
			if self.mp.in_shop(PETROL_SHOP, self.r, self.c):
				self.try_fill_p()
			elif self.mp.in_shop(GAS_SHOP, self.r, self.c):
				self.try_fill_g()
			elif self.mp.in_shop(ORES_SHOP, self.r, self.c):
				self.try_sell()
			elif self.mp.in_shop(DRILL_SHOP, self.r, self.c):
				glb.pages.append(Page_Shop(self.dr))
				self.upgrade = 1

		self.cloud_update()
		self.sky_spg.update()
		self.cld_spg.update()
		self.bg_spg.update()
		self.dr_spg.update()
		if self.show_info:
			self.refresh_info()
		return PAGE_NONE

	def try_move(self, d, speedup):
		nr, nc = self.r + D_XY[d][0], self.c + D_XY[d][1]
		if not self.mp.in_bound(nr, nc):
			return
		if self.dr.p_cur <= 0:
			return
		if self.dr.g_cur <= 0:
			speedup = 0
		self.speed = tool.get_speed_level(self.mp.mp[nr][nc], self.dr.rgd_l, self.dr.eng_l, speedup)
		if self.speed[0] == 0:
			return
		self.nr, self.nc = nr, nc
		self.is_moving = 1
		self.mv_timer = self.speed[1]
		self.pixel = 0
		if d == self.dir and self.speedup == speedup:
			return
		self.dr_spg.empty()
		self.dir = d
		self.speedup = speedup
		self.dr_spg.add(self.dr_h[d])
		self.dr_spg.add(self.dr_b[d])
		self.dr_spg.add(self.dr_f[speedup][d])

	def move(self):
		if self.dr.p_cur <= 0:
			self.is_moving = 0
			return
		self.dr.p_cur -= 1 * (self.dr.eng_l + 1)
		if self.dr.p_cur < 0:
			self.dr.p_cur = 0
		rd, rsp, = D_MP[self.dir], 0
		self.mv_timer -= 1
		if self.mv_timer == 0:
			self.pixel += self.speed[0]
			rsp = self.speed[0]
			self.mv_timer = self.speed[1]
		if self.pixel == BLOCK_SZ:
			self.r, self.c = self.nr, self.nc
			if self.speedup:
				self.dr.g_cur -= 1
			self.pixel = 0
			self.is_moving = 0
			self.move_finish()
		if rsp == 0:
			return
		self.sky_spg.move(rd, rsp)
		self.cld_spg.move(rd, rsp)
		self.bg_spg.move(rd, rsp)
		self.mp_spg.move(rd, rsp)

	def move_finish(self):
		glb.achieve.vals['tot_move'] += 1
		if self.r <= self.mp.g_level:
			return
		if self.mp.mp[self.r][self.c] != EMPTY:
			glb.achieve.vals[self.mp.mp[self.r][self.c]] += 1
			if self.mp.mp[self.r][self.c] != DIRT:
				glb.achieve.vals['tot_ore'] += 1
				if self.dr.o_cur < self.dr.o_cap:
					self.dr.carry += ORES_VALUE[self.mp.mp[self.r][self.c]]
					self.dr.o_cur += 1
			self.mp.mp[self.r][self.c] = EMPTY
			self.mp_sp[self.r][self.c].kill()

	def try_fill_p(self):
		pre = self.dr.p_cur
		self.dr.p_cur = min(self.dr.p_cap, self.dr.p_cur + self.dr.money // PETROL_COST)
		self.dr.money -= (self.dr.p_cur - pre) * PETROL_COST

	def try_fill_g(self):
		pre = self.dr.g_cur
		self.dr.g_cur = min(self.dr.g_cap, self.dr.g_cur + self.dr.money // GAS_COST)
		self.dr.money -= (self.dr.g_cur - pre) * GAS_COST

	def try_sell(self):
		glb.achieve.vals['tot_money'] += self.dr.carry
		self.dr.money += self.dr.carry
		self.dr.carry = self.dr.o_cur = 0

	def cloud_update(self):
		for sp in self.cld_spg.sprites():
			if isinstance(sp, SpriteEasy):
				continue
			if not sp.check_in_map(self.sky.rect.x, self.mp.m*BLOCK_SZ):
				logging.debug('remove')
				self.cld_spg.remove(sp)
				self.cloud_num -= 1
		if self.cloud_num >= self.cloud_num_max:
			return
		if random.randint(1, 100) <= CLOUD_GEN_SPEED:
			self.cld_spg.add(self.generate_cloud())
			self.cloud_num += 1

	def switch_info(self):
		if self.show_info:
			self.list.pop()
		else:
			self.list.append(self.info)
		self.show_info ^= 1

	def refresh_info(self):
		self.info.clear()
		diff = datetime.now() - self.pre_time
		self.pre_time = datetime.now()
		self.info.add_row(f'FPS: {int(1 / diff.total_seconds())}')
		self.info.add_row(f'屏幕大小: {SCR_N}行, {SCR_M}列, 地图大小:{self.mp.n}行, {self.mp.m}列, 当前在: {self.r}行, {self.c}列')
		self.info.add_row(f'当前一共有 {self.tree_num} 棵树, 当前一共有 {self.cloud_num} 朵云')
		self.info.add_row(f'金钱: {self.dr.money}')
		self.info.add_row(f'油量: {self.dr.p_cur} / {self.dr.p_cap}, 推进剂: {self.dr.g_cur} / {self.dr.g_cap}')
		self.info.add_row(f'携带矿石: {self.dr.o_cur} / {self.dr.o_cap}, 当带矿石的价值: {self.dr.carry}')
		self.info.add_row(f'钻头等级: {self.dr.rgd_l}, 引擎等级: {self.dr.eng_l}')
		self.info.add_row(f'油箱等级: {self.dr.p_cap_l}, 推进剂等级: {self.dr.eng_l}, 矿物容量等级: {self.dr.o_cap_l}')
		s = '当前在地下'
		if self.r == self.mp.g_level:
			s = '当前在地上'
		if self.mp.in_shop(PETROL_SHOP, self.r, self.c):
			s = '当前位于加油站'
		if self.mp.in_shop(GAS_SHOP, self.r, self.c):
			s = '当前位于加气站'
		if self.mp.in_shop(ORES_SHOP, self.r, self.c):
			s = '当前位于售卖处'
		if self.mp.in_shop(DRILL_SHOP, self.r, self.c):
			s = '当前位于升级店'
		self.info.add_row(s)
		self.info.add_row(f'存档信息:')
		for i in range(1, 11, 2):
			s = f'  存档 {i}:' + glb.log.logs_info[i] + f'  存档 {i+1}:' + glb.log.logs_info[i+1]
			self.info.add_row(s)
		self.info.add_row(f'档案:')
		self.info.add_row(f'{BLK_DATA[DIRT]["name"]}: {glb.achieve.vals[DIRT]}, {BLK_DATA[COAL]["name"]}: {glb.achieve.vals[COAL]}')
		self.info.add_row(f'{BLK_DATA[COPPER]["name"]}: {glb.achieve.vals[COPPER]}, {BLK_DATA[SILVER]["name"]}: {glb.achieve.vals[SILVER]}')
		self.info.add_row(f'{BLK_DATA[GOLD]["name"]}: {glb.achieve.vals[GOLD]}, {BLK_DATA[AMETHYST]["name"]}: {glb.achieve.vals[AMETHYST]}')
		self.info.add_row(f'{BLK_DATA[EMERALD]["name"]}: {glb.achieve.vals[EMERALD]}, {BLK_DATA[SAPPHIRE]["name"]}: {glb.achieve.vals[SAPPHIRE]}')
		self.info.add_row(f'{BLK_DATA[RUBY]["name"]}: {glb.achieve.vals[RUBY]}, {BLK_DATA[DIAMOND]["name"]}: {glb.achieve.vals[DIAMOND]}')
		self.info.add_row(f'总矿物: {glb.achieve.vals["tot_ore"]}')
		self.info.add_row(f'总金钱: {glb.achieve.vals["tot_money"]}')
		self.info.add_row(f'总移动距离: {glb.achieve.vals["tot_move"]}')
		if self.is_moving:
			self.info.add_row(f'当前正在移动')
			self.info.add_row(f'移动方向为，行：{D_XY[self.dir][0]} 列：{D_XY[self.dir][1]}')
			self.info.add_row(f'当前的移动速度为, {self.speed[0]}/{self.speed[1]} 像素每帧')
		else:
			self.info.add_row(f'当前没在移动')

