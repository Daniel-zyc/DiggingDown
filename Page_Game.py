from Constant import *
from Control import Control
from Page import Page
from Map import Map
from Drill import Drill
from SpriteGroup import SpriteGroup
from Sprite import Sprite
from SpriteEasy import SpriteEasy
from SpriteMulti import SpriteMulti
from datetime import datetime
from Page_Pause import Page_Pause
from Page_DShop import Page_DShop
from Page_Key import Page_Key
from Page_Info import Page_Info
from Page_Achieve import Page_Achieve
from Menu import MenuText
import Global as glb
import random
import threading


class Sprite_Cloud(SpriteEasy):
	def __init__(self, idx, d, spd, x, y):
		super().__init__(CLD_IMG_URL.format(idx), x, y, random.random() / 2 + 1)
		if d == D_R:
			self.rect.topright = (x, y)
		self.mv_timer = SPEED_LEVEL[0][spd][1]
		self.d, self.spd = BG_DIR_MP[d], spd

	def update(self):
		self.mv_timer -= 1
		if self.mv_timer == 0:
			self.move(self.d, SPEED_LEVEL[0][self.spd][0])
			self.mv_timer = SPEED_LEVEL[0][self.spd][1]


class Sprite_Bird(SpriteMulti):
	def __init__(self, idx, d, spd, x, y):
		super().__init__(BIRD_IMG_URL.format(idx), x, y)
		if d == D_R:
			self.rect.topright = (x, y)
		else:
			for i in range(0, len(self.images)):
				self.images[i] = pg.transform.flip(self.images[i], True, False)
		for img in self.images:
			img.set_colorkey((0, 0, 0))
		self.mv_timer = SPEED_LEVEL[0][spd][1]
		self.d, self.spd = BG_DIR_MP[d], spd

	def update(self):
		self.mv_timer -= 1
		if self.mv_timer == 0:
			self.move(self.d, SPEED_LEVEL[0][self.spd][0])
			self.mv_timer = SPEED_LEVEL[0][self.spd][1]
		self.roll_image()


class Sprite_Tree(SpriteEasy):
	def __init__(self, idx, x, y):
		super().__init__(TREE_IMG_URL.format(idx), x, y, 1.5)
		self.rect.bottomleft = (x, y)
		self.rect.y += 10


class Sprite_Shop(SpriteMulti):
	def __init__(self, idx, x, y):
		super().__init__(SHOP_IMG_URL[idx], x, y)
		for i in range(0, len(self.images)):
			if idx == O_SHOP:
				self.images[i] = pg.transform.scale_by(self.images[i], 2.5)
			else:
				self.images[i] = pg.transform.scale2x(self.images[i])
			self.images[i].set_colorkey(SHOP_COLORKEY[idx])
		self.image = self.images[self.image_idx]
		self.rect = self.image.get_rect()
		self.rect.bottomleft = (x, y)


class Background_Sp:
	def __init__(self, mp: Map, dr: Drill):
		self.mp, self.dr = mp, dr
		self.w = self.mp.m * BLOCK_SZ
		self.cloud_num = self.cloud_num_max = CLD_NUM_MAX * self.mp.m // BG_DENS_LEN
		self.tree_num = self.tree_num_max = TREE_NUM_MAX * self.mp.m // BG_DENS_LEN
		self.bird_num = self.bird_num_max = BIRD_NUM_MAX * self.mp.m // BG_DENS_LEN
		self.sky, self.cld, self.tree, self.bird, self.shop = SpriteGroup(), SpriteGroup(), SpriteGroup(), SpriteGroup(), SpriteGroup()
		self.wind_dir = BG_DIR[random.randint(0, 1)]
		self.mv_pixel = self.mv_unit = 0
		self.__init_sky()
		self.__init_cld()
		self.__init_bird()
		self.__init_tree()
		self.__init_shop()

	def __init_sky(self):
		idx = random.randint(0, SKY_LEN - 1)
		x, y = scr_b_to_p(1, self.mp.m // 3 - 1, self.mp.r, self.mp.c)
		x -= SCR_W
		endx, endy = scr_b_to_p(1, self.mp.m * 2 // 3 + 1, self.mp.r, self.mp.c)
		endx += SCR_W
		sp = SpriteEasy(SKY_IMG_URL.format(idx), x, y)
		self.sky.add(sp)
		x += sp.rect.w
		while x < endx:
			sp = SpriteEasy(SKY_IMG_URL.format(idx), x, y)
			self.sky.add(sp)
			x += sp.rect.w

	def __init_cld(self):
		self.cloud_num = 0

	def __generate_cld(self):
		spd = random.randint(CLD_SPD[0], CLD_SPD[1])
		idx = random.randint(0, CLD_LEN - 1)
		x, y = -random.randint(1, SCR_W), random.randint(0, SCR_H // 5)
		if self.wind_dir == D_L:
			x = SCR_W + random.randint(1, SCR_W)
		y -= self.mp.r * BLOCK_SZ
		return Sprite_Cloud(idx, self.wind_dir, spd, x, y)

	def __init_bird(self):
		self.bird_num = 0

	def __generate_bird(self):
		spd = random.randint(BIRD_SPD[0], BIRD_SPD[1])
		idx = random.randint(0, BIRD_LEN - 1)
		x, y = -random.randint(1, SCR_W), random.randint(0, SCR_H // 5)
		d = BG_DIR[random.randint(0, 1)]
		if d == D_L:
			x = SCR_W + random.randint(1, SCR_W)
		y -= self.mp.r * BLOCK_SZ
		return Sprite_Bird(idx, d, spd, x, y)

	def __init_tree(self):
		self.tree_num = random.randint(0, self.tree_num_max)
		for i in range(0, self.tree_num):
			self.tree.add(self.__generate_tree())

	def __generate_tree(self):
		idx = random.randint(0, TREE_LEN - 1)
		c = random.randint(0, self.mp.m)
		x, y = map_b_to_p(1, c, self.mp.r, self.mp.c)
		return Sprite_Tree(idx, x, y)

	def __init_shop(self):
		for key, range in SHOP_R.items():
			x, y = map_b_to_p(1, range[0] + self.mp.reborn_C, self.mp.r, self.mp.c)
			self.shop.add(Sprite_Shop(key, x, y))

	def update(self):
		self.cld.update()
		self.shop.update()
		for sp in self.cld.sprites():
			if not pg.sprite.spritecollide(sp, self.sky, False):
				sp.kill()
				self.cloud_num -= 1
		self.bird.update()
		for sp in self.bird.sprites():
			if not pg.sprite.spritecollide(sp, self.sky, False):
				sp.kill()
				self.bird_num -= 1
		if self.mp.r > SCR_CEN_R:
			return
		if self.cloud_num < self.cloud_num_max and random.randint(1, CLD_GEN_SPD[1]) <= CLD_GEN_SPD[0]:
			self.cld.add(self.__generate_cld())
			self.cloud_num += 1
		if self.bird_num < self.cloud_num_max and random.randint(1, BIRD_GEN_SPD[1]) <= BIRD_GEN_SPD[0]:
			self.bird.add(self.__generate_bird())
			self.bird_num += 1

	def move(self, d, spd):
		if d == D_MP[D_U] or d == D_MP[D_D]:
			self.tree.move(d, spd)
			self.shop.move(d, spd)
			self.cld.move(d, spd)
			self.sky.move(d, spd)
			self.bird.move(d, spd)
			return
		if d == D_MP[D_L]:
			self.mv_pixel -= spd
		else:
			self.mv_pixel += spd
		tmp = abs(self.mv_pixel // 3 - self.mv_unit)
		self.mv_unit = self.mv_pixel // 3
		self.tree.move(d, spd)
		self.shop.move(d, spd)
		self.cld.move(d, tmp)
		self.sky.move(d, tmp)
		self.bird.move(d, tmp)

	def draw(self, scr):
		if self.mp.r > SCR_CEN_R:
			return
		scr_rect = scr.get_rect()
		for sp in self.sky.sprites():
			if sp.rect.colliderect(scr_rect):
				sp.draw(scr)
		for sp in self.cld.sprites():
			if sp.rect.colliderect(scr_rect):
				sp.draw(scr)
		for sp in self.tree.sprites():
			if sp.rect.colliderect(scr_rect):
				sp.draw(scr)
		for sp in self.bird.sprites():
			if sp.rect.colliderect(scr_rect):
				sp.draw(scr)
		for sp in self.shop.sprites():
			if sp.rect.colliderect(scr_rect):
				sp.draw(scr)

	def empty(self):
		self.sky.empty()
		self.cld.empty()
		self.tree.empty()
		self.bird.empty()
		self.shop.empty()


class Sprite_Block(Sprite):
	def __init__(self, tp, x, y):
		super().__init__()
		self.image = image_buf[tp]
		if is_chest(tp):
			self.image = pg.transform.scale(self.image, (26, 26))
			x -= 1
			y -= 1
		self.rect = self.image.get_rect()
		self.rect.x, self.rect.y = x, y


class Sprite_NPC(Sprite):
	def __init__(self, tp, x, y):
		super().__init__()
		self.image = image_buf[tp]
		self.image.set_colorkey((0, 0, 0))
		self.rect = self.image.get_rect()
		self.rect.midbottom = (x + BLOCK_SZ // 2 - 1, y + BLOCK_SZ)
		self.npc = tp

	def update(self):
		if random.randint(1, NPC_MOVE[1]) > random.randint(1, NPC_MOVE[0]):
			return
		self.image = pg.transform.flip(self.image, True, False)


class Map_Sp:
	def __init__(self, mp: Map, dr: Drill):
		self.mp, self.dr = mp, dr
		image_buf[UNDER] = pg.image.load(UNDER_IMG_URL.format(random.randint(0, UNDER_LEN - 1)))
		image_buf[CAVE] = pg.image.load(CAVE_IMG_URL.format(random.randint(0, CAVE_LEN - 1)))
		self.map = [[None] * (self.mp.m + 1) for i in range(0, self.mp.n + 1)]
		self.fog = [[None] * (self.mp.m + 1) for i in range(0, self.mp.n + 1)]
		self.npc = SpriteGroup()
		self.old_r, self.old_c = self.mp.r, self.mp.c
		self.create()
		self.erase_fog(self.dr.r, self.dr.c)

	def add_block(self, i, j):
		if not self.mp.in_dirt(i, j):
			return
		x, y = map_b_to_p(i, j, self.mp.r, self.mp.c)
		if self.mp.fog[i][j]:
			self.fog[i][j] = Sprite_Block(FOG, x, y)
		elif is_dirt(self.mp.mp[i][j]) or is_ore(self.mp.mp[i][j]) or is_chest(self.mp.mp[i][j]):
			self.map[i][j] = Sprite_Block(self.mp.mp[i][j], x, y)
		if is_NPC(self.mp.mp[i][j]):
			self.npc.add(Sprite_NPC(self.mp.mp[i][j], x, y))
		if self.mp.mp[i][j] != EMPTY and not is_NPC(self.mp.mp[i][j]):
			return
		if self.mp.in_under(i, j):
			self.map[i][j] = Sprite_Block(UNDER, x, y)
		else:
			self.map[i][j] = Sprite_Block(CAVE, x, y)

	def remove_npc(self, idx):
		for sp in self.npc.sprites():
			if sp.npc == idx:
				self.npc.remove(sp)
				break

	def remove_block(self, i, j):
		if not self.mp.in_dirt(i, j):
			return
		if self.map[i][j] is not None:
			self.map[i][j].kill()
		if self.fog[i][j] is not None:
			self.fog[i][j].kill()
		self.map[i][j] = self.fog[i][j] = None
		if is_NPC(self.mp.mp[i][j]):
			self.remove_npc(self.mp.mp[i][j])

	def create(self):
		self.old_r, self.old_c = self.mp.r, self.mp.c
		for i in range(self.old_r - SCR_CEN_R - PRE_LOAD + 1, self.old_r + SCR_CEN_R + PRE_LOAD):
			for j in range(self.old_c - SCR_CEN_C - PRE_LOAD + 1, self.old_c + SCR_CEN_C + PRE_LOAD):
				self.add_block(i, j)

	def in_preload_range(self, r, c, rr, cc):
		return rr - SCR_CEN_R - PRE_LOAD < r < rr + SCR_CEN_R + PRE_LOAD and cc - SCR_CEN_C - PRE_LOAD < c < cc + SCR_CEN_C + PRE_LOAD

	def recreate(self):
		if self.mp.r != self.old_r:
			r, nr = self.old_r - SCR_CEN_R - PRE_LOAD + 1, self.mp.r + SCR_CEN_R + PRE_LOAD - 1
			if self.mp.r < self.old_r:
				r, nr = self.old_r + SCR_CEN_R + PRE_LOAD - 1, self.mp.r - SCR_CEN_R - PRE_LOAD + 1
			for j in range(self.mp.c - SCR_CEN_C - PRE_LOAD + 1, self.mp.c + SCR_CEN_C + PRE_LOAD):
				self.add_block(nr, j)
				self.remove_block(r, j)
		else:
			c, nc = self.old_c - SCR_CEN_C - PRE_LOAD + 1, self.mp.c + SCR_CEN_C + PRE_LOAD - 1
			if self.mp.c < self.old_c:
				c, nc = self.old_c + SCR_CEN_C + PRE_LOAD - 1, self.mp.c - SCR_CEN_C - PRE_LOAD + 1
			for i in range(self.mp.r - SCR_CEN_R - PRE_LOAD + 1, self.mp.r + SCR_CEN_R + PRE_LOAD):
				self.add_block(i, nc)
				self.remove_block(i, c)
		self.old_r, self.old_c = self.mp.r, self.mp.c

	def erase_fog(self, r, c):
		for i in range(r - FOG_RAD, r + FOG_RAD + 1):
			for j in range(c - FOG_RAD, c + FOG_RAD + 1):
				if not self.mp.in_dirt(i, j) or fog_dist(i, j, r, c) > FOG_RAD or not self.mp.fog[i][j]:
					continue
				self.mp.fog[i][j] = 0
				self.fog[i][j] = None
				x, y = map_b_to_p(i, j, self.mp.r, self.mp.c)
				if is_dirt(self.mp.mp[i][j]) or is_ore(self.mp.mp[i][j]) or is_chest(self.mp.mp[i][j]):
					self.map[i][j] = Sprite_Block(self.mp.mp[i][j], x, y)
				elif self.mp.in_under(i, j):
					self.map[i][j] = Sprite_Block(UNDER, x, y)
				else:
					self.map[i][j] = Sprite_Block(CAVE, x, y)

	def to_empty(self, r, c):
		if self.mp.mp[r][c] == EMPTY or r == 0:
			return
		x, y = map_b_to_p(r, c, self.mp.r, self.mp.c)
		if self.mp.in_under(r, c):
			self.map[r][c] = Sprite_Block(UNDER, x, y)
		else:
			self.map[r][c] = Sprite_Block(CAVE, x, y)
		if is_NPC(self.mp.mp[r][c]):
			self.remove_npc(self.mp.mp[r][c])
		self.mp.mp[r][c] = EMPTY

	def update_map(self, r, c):
		self.erase_fog(r, c)
		self.to_empty(r, c)
		if self.mp.r != self.old_r or self.mp.c != self.old_c:
			self.recreate()

	def move(self, d, sp):
		self.npc.move(d, sp)
		for i in range(self.old_r - SCR_CEN_R - PRE_LOAD + 1, self.old_r + SCR_CEN_R + PRE_LOAD):
			for j in range(self.old_c - SCR_CEN_C - PRE_LOAD + 1, self.old_c + SCR_CEN_C + PRE_LOAD):
				if not self.mp.in_dirt(i, j):
					continue
				if self.map[i][j] is not None:
					self.map[i][j].move(d, sp)
				if self.fog[i][j] is not None:
					self.fog[i][j].move(d, sp)

	def draw(self, scr):
		self.npc.update()
		for i in range(self.old_r - SCR_CEN_R - PRE_LOAD + 1, self.old_r + SCR_CEN_R + PRE_LOAD):
			for j in range(self.old_c - SCR_CEN_C - PRE_LOAD + 1, self.old_c + SCR_CEN_C + PRE_LOAD):
				if not self.mp.in_dirt(i, j) or self.map[i][j] is None:
					continue
				self.map[i][j].draw(scr)
		self.npc.draw(scr)
		for i in range(self.old_r - SCR_CEN_R - PRE_LOAD + 1, self.old_r + SCR_CEN_R + PRE_LOAD):
			for j in range(self.old_c - SCR_CEN_C - PRE_LOAD + 1, self.old_c + SCR_CEN_C + PRE_LOAD):
				if not self.mp.in_dirt(i, j) or self.fog[i][j] is None:
					continue
				self.fog[i][j].draw(scr)

	def empty(self):
		self.fog.clear()
		self.npc.empty()
		self.map.clear()


class Sprite_Head(Sprite):
	def __init__(self, x, y, d, l):
		super().__init__()
		if d <= 2:
			self.image = pg.image.load(DR_IMG_URL[HEAD].format(d, l))
		else:
			self.image = pg.image.load(DR_IMG_URL[HEAD].format(d - 2, l))
			if d == D_L:
				self.image = pg.transform.flip(self.image, True, False)
			else:
				self.image = pg.transform.flip(self.image, False, True)
		self.image.set_colorkey((255, 255, 255))
		self.rect = self.image.get_rect()
		self.rect.x, self.rect.y = x, y
		self.dir = BG_DIR_MP[d]
		self.shake_idx = 0

	def update(self):
		self.rect.x += D_XY[self.dir][0] * HEAD_SHAKE[self.shake_idx]
		self.rect.y += D_XY[self.dir][1] * HEAD_SHAKE[self.shake_idx]
		self.shake_idx += 1
		self.shake_idx %= len(HEAD_SHAKE)


class Sprite_Body(Sprite):
	def __init__(self, x, y, d, l):
		super().__init__()
		if d <= 2:
			self.image = pg.image.load(DR_IMG_URL[BODY].format(d, l))
		else:
			self.image = pg.image.load(DR_IMG_URL[BODY].format(d - 2, l))
			if d == D_L:
				self.image = pg.transform.flip(self.image, True, False)
			else:
				self.image = pg.transform.flip(self.image, False, True)
		self.image.set_colorkey((255, 255, 255))
		self.rect = self.image.get_rect()
		self.rect.x, self.rect.y = x, y


class Sprite_Flame(Sprite):
	def __init__(self, tp, x, y, d, l):
		super().__init__()
		if d <= 2:
			self.image = pg.image.load(DR_IMG_URL[tp].format(d, l))
		else:
			self.image = pg.image.load(DR_IMG_URL[tp].format(d - 2, l))
			if d == D_L:
				self.image = pg.transform.flip(self.image, True, False)
			else:
				self.image = pg.transform.flip(self.image, False, True)
		self.image.set_colorkey((255, 255, 255))
		self.rect = self.image.get_rect()
		self.rect.x, self.rect.y = x, y
		self.dir = d
		self.shake_idx = 0

	def update(self):
		self.rect.x += D_XY[self.dir][0] * FLAME_SHAKE[self.shake_idx]
		self.rect.y += D_XY[self.dir][1] * FLAME_SHAKE[self.shake_idx]
		self.shake_idx += 1
		self.shake_idx %= len(FLAME_SHAKE)
		self.dir += 1
		if self.dir > 4:
			self.dir = 1


class Drill_Sp:
	def __init__(self, mp: Map, dr: Drill):
		self.mp, self.dr = mp, dr
		self.heads = self.get_drill_sp(HEAD)
		self.bodys = self.get_drill_sp(BODY)
		self.sflames = self.get_drill_sp(SFLAME)
		self.lflames = self.get_drill_sp(LFLAME)
		self.head, self.body, self.flame = SpriteGroup(), SpriteGroup(), SpriteGroup()
		self.dir, self.is_moving, self.speedup, self.is_drilling = D_R, 0, 0, 0
		self.update()

	def update(self):
		self.head.empty()
		self.body.empty()
		self.flame.empty()
		self.head.add(self.heads[self.dir])
		self.body.add(self.bodys[self.dir])
		if self.is_moving:
			if self.speedup:
				self.flame.add(self.lflames[self.dir])
			else:
				self.flame.add(self.sflames[self.dir])
		if self.is_drilling:
			self.head.update()
		if self.is_moving:
			self.flame.update()

	def get_drill_sp(self, part):
		ret = [None]
		xx, yy = [SCR_CEN_R] * 5, [SCR_CEN_C] * 5
		if part == HEAD:
			for d in range(1, 5):
				xx[d], yy[d] = xx[d] + D_XY[d][0], yy[d] + D_XY[d][1]
				xx[d], yy[d] = dr_b_to_p(xx[d], yy[d], self.dr.r, self.dr.c, self.mp.r, self.mp.c)
				ret.append(Sprite_Head(xx[d], yy[d], d, self.dr.rgd_l))
		elif part == SFLAME:
			for d in range(1, 5):
				xx[d], yy[d] = xx[d] - D_XY[d][0], yy[d] - D_XY[d][1]
				xx[d], yy[d] = dr_b_to_p(xx[d], yy[d], self.dr.r, self.dr.c, self.mp.r, self.mp.c)
				ret.append(Sprite_Flame(SFLAME, xx[d], yy[d], d, self.dr.g_l))
		elif part == LFLAME:
			for d in range(1, 5):
				xx[d], yy[d] = xx[d] - D_XY[d][0], yy[d] - D_XY[d][1]
				xx[d], yy[d] = dr_b_to_p(xx[d], yy[d], self.dr.r, self.dr.c, self.mp.r, self.mp.c)
				ret.append(Sprite_Flame(LFLAME, xx[d], yy[d], d, self.dr.g_l))
		else:
			for d in range(1, 5):
				xx[d], yy[d] = dr_b_to_p(xx[d], yy[d], self.dr.r, self.dr.c, self.mp.r, self.mp.c)
				ret.append(Sprite_Body(xx[d], yy[d], d, self.dr.h_l))
		return ret

	def move(self, d, sp):
		for i in range(1, 5):
			self.heads[i].move(d, sp)
			self.bodys[i].move(d, sp)
			self.sflames[i].move(d, sp)
			self.lflames[i].move(d, sp)

	def draw(self, scr):
		self.head.draw(scr)
		self.flame.draw(scr)
		self.body.draw(scr)

	def empty(self):
		self.head.empty()
		self.body.empty()
		self.flame.empty()


class Game_Info:
	pass


class NPC_Sp:
	def __init__(self, mp: Map):
		self.mp = mp
		self.npcs = [[], []]
		r, c = SCR_N - 1, SCR_CEN_C - NPC_TOT // 2 * 2
		for npc in NPCS:
			x, y = b_to_p(r, c)
			self.npcs[0].append(Sprite_NPC(npc, x, y))
			self.npcs[0][-1].image = load_img(NPC_IMG_URL.format(npc - NPCS[0]))
			self.npcs[0][-1].image.set_colorkey((0, 0, 0))
			self.npcs[0][-1].image.set_alpha(96)
			self.npcs[1].append(Sprite_NPC(npc, x, y))
			c += 2

	def draw(self, scr):
		for npc in NPCS:
			idx = npc - NPCS[0]
			self.npcs[self.mp.npc[npc]][idx].draw(scr)

	def empty(self):
		self.npcs = None


class Ore_Sp:
	def __init__(self, mp: Map, dr: Drill):
		self.mp, self.dr = mp, dr
		self.ores = []
		self.text = []
		self.xy = []
		r, c = SCR_N - 4, SCR_CEN_C - ORE_TOT // 2 * 3
		for ore in ORES:
			x, y = b_to_p(r, c)
			self.ores.append(Sprite_Block(ore, x, y))
			x += BLOCK_SZ + BLOCK_SZ
			y += BLOCK_SZ // 2
			self.xy.append([x, y])
			self.text.append(MenuText(f'{self.dr.carry[ore]}', 10, posx = x, posy = y, absolute = True))
			c += 3

	def draw(self, scr):
		for ore in self.ores:
			ore.draw(scr)
		for text in self.text:
			text.draw(scr)

	def update(self, ore = None):
		if ore is None:
			self.text = []
			for ore in ORES:
				idx = ore - ORES[0]
				self.text.append(MenuText(f'{self.dr.carry[ore]}', 10, posx = self.xy[idx][0], posy = self.xy[idx][1], absolute = True))
		else:
			idx = ore - ORES[0]
			self.text[idx] = MenuText(f'{self.dr.carry[ore]}', 10, posx = self.xy[idx][0], posy = self.xy[idx][1], absolute = True)

	def empty(self):
		self.ores = self.text = None


class Sprite_Bar(Sprite):
	def __init__(self, name, vals, color, top, w = SCR_W // 4, h = 36, border = 4, padding = 24, border_color = (0, 0, 0), bg_color = (63, 63, 63), t_color = (255, 255, 255)):
		font = pg.font.Font(PIXEL_FONT_URL, 24)
		self.image = pg.Surface((w + border * 2, h + border * 2))
		self.rect = self.image.get_rect()
		self.image.fill(border_color)
		len = w * vals[0] // vals[1]
		pg.draw.rect(self.image, bg_color, (border, border, w, h))
		pg.draw.rect(self.image, color, (border, border, len, h))
		text = font.render(f'{name}: {vals[0]} | {vals[1]}', True, t_color)
		rect = text.get_rect()
		rect.center = self.rect.center
		rect.left = self.rect.left + border + 14
		self.image.blit(text, rect)
		self.rect = self.image.get_rect()
		self.rect.topright = (SCR_W - padding, top + padding)


class Bar_Sp:
	def __init__(self, dr):
		self.dr = dr
		self.oldp, self.oldp_max = self.dr.p, self.dr.p_max
		self.oldh, self.oldh_max = self.dr.h, self.dr.h_max
		self.oldg, self.oldg_max = self.dr.g, self.dr.g_max
		self.oldo, self.oldo_max = self.dr.o, self.dr.o_max
		self.oldm = self.dr.money
		self.bars = []
		self.bars.append(Sprite_Bar('燃油量', (self.dr.p, self.dr.p_max), P_COLOR, 0))
		self.bars.append(Sprite_Bar('血量  ', (self.dr.h, self.dr.h_max), H_COLOR, self.bars[-1].rect.bottom))
		self.bars.append(Sprite_Bar('燃气量', (self.dr.g, self.dr.g_max), G_COLOR, self.bars[-1].rect.bottom))
		self.bars.append(Sprite_Bar('矿物量', (self.dr.o, self.dr.o_max), O_COLOR, self.bars[-1].rect.bottom))
		self.bars.append(MenuText(f'金钱: {self.dr.money}', 24, posy = 0.05))

	def draw(self, scr):
		for bar in self.bars:
			bar.draw(scr)

	def update(self):
		if self.oldp != self.dr.p or self.oldp_max != self.dr.p_max:
			self.bars[0] = Sprite_Bar('燃油量', (self.dr.p, self.dr.p_max), P_COLOR, 0)
		if self.oldh != self.dr.h or self.oldh_max != self.dr.h_max:
			self.bars[1] = Sprite_Bar('血量  ', (self.dr.h, self.dr.h_max), H_COLOR, self.bars[0].rect.bottom)
		if self.oldg != self.dr.g or self.oldg_max != self.dr.g_max:
			self.bars[2] = Sprite_Bar('燃气量', (self.dr.g, self.dr.g_max), G_COLOR, self.bars[1].rect.bottom)
		if self.oldo != self.dr.o or self.oldo_max != self.dr.o_max:
			self.bars[3] = Sprite_Bar('矿物量', (self.dr.o, self.dr.o_max), O_COLOR, self.bars[2].rect.bottom)
		if self.oldm != self.dr.money:
			self.bars[4] = MenuText(f'金钱: {self.dr.money}', 24, posy = 0.05)
		self.oldp, self.oldp_max = self.dr.p, self.dr.p_max
		self.oldh, self.oldh_max = self.dr.h, self.dr.h_max
		self.oldg, self.oldg_max = self.dr.g, self.dr.g_max
		self.oldo, self.oldo_max = self.dr.o, self.dr.o_max


class Page_Game(Page):
	def __init__(self, log_id = 0):
		super().__init__()
		self.update_range = pg.Rect(0, 0, SCR_W, SCR_H)
		self.mp = Map()
		self.dr = Drill()
		if log_id != 0:
			glb.log.log_read(log_id, self.mp, self.dr)
		else:
			self.mp.init_new()
			self.dr.init_new(self.mp.reborn_R, self.mp.reborn_C)
		self.old_rgd, self.old_eng, self.old_h = self.dr.rgd_l, self.dr.eng_l, self.dr.h_l
		self.bg = Background_Sp(self.mp, self.dr)
		self.map = Map_Sp(self.mp, self.dr)
		self.drill = Drill_Sp(self.mp, self.dr)
		self.show_bar = 1
		self.bar = Bar_Sp(self.dr)
		self.show_npc = 1
		self.npc = NPC_Sp(self.mp)
		self.show_ore = 1
		self.ore = Ore_Sp(self.mp, self.dr)
		self.frame_cnt = self.show_info = self.pre_fps = 0
		self.pre_time = datetime.now()
		self.info = Game_Info(self)
		self.speed, self.pixel, self.nr, self.nc, self.mv_timer = SPEED_LEVEL[0][0], 0, 0, 0, SPEED_LEVEL[0][0][1]

	def refresh(self, ctrl: Control):
		self.update_fps()
		if ctrl.get_key(CTRL_ESC):
			glb.pages.append(Page_Pause(self.mp, self.dr))
			return PAGE_NONE
		if ctrl.get_key(CTRL_TAB):
			self.show_info += 1
			self.show_info %= 6
		if ctrl.get_key(CTRL_INTER[1]):
			self.show_npc ^= 1
		if ctrl.get_key(CTRL_INTER[2]):
			self.show_ore ^= 1
		if ctrl.get_key(CTRL_I):
			glb.pages.append(Page_Info())
			return PAGE_NONE
		if ctrl.get_key(CTRL_J):
			glb.pages.append(Page_Achieve())
			return PAGE_NONE
		if ctrl.get_key(CTRL_K):
			glb.pages.append(Page_Key())
			return PAGE_NONE
		if not self.drill.is_moving:
			key = ctrl.get_press(CTRL_L, CTRL_R, CTRL_D, CTRL_U)
			if key:
				self.try_move(key, ctrl.get_press(CTRL_SH) != CTRL_NONE)
			key = ctrl.get_key(CTRL_ENTER)
			if key:
				if self.mp.in_shop(P_SHOP, self.dr.r, self.dr.c):
					self.try_fillp()
				elif self.mp.in_shop(G_SHOP, self.dr.r, self.dr.c):
					self.try_fillg()
				elif self.mp.in_shop(R_SHOP, self.dr.r, self.dr.c):
					self.try_repair()
				elif self.mp.in_shop(O_SHOP, self.dr.r, self.dr.c):
					self.try_sell()
				elif self.mp.in_shop(D_SHOP, self.dr.r, self.dr.c):
					glb.pages.append(Page_DShop(self.dr, self.drill))
					return PAGE_NONE
		self.drill.update()
		if self.drill.is_moving:
			self.move()
		self.bg.update()
		if self.show_info:
			self.info.update(self.show_info)
		if self.show_bar:
			self.bar.update()
		return PAGE_NONE

	def try_fillp(self):
		pre, nxt = self.dr.p, min(self.dr.p_max, self.dr.p + self.dr.money * P_COST[1] // P_COST[0])
		if pre == nxt and nxt != self.dr.p_max:
			glb.show_WN('没钱加油')
			return
		elif pre == nxt:
			glb.show_WN('无需加油', color = DARK_GREEN)
			return
		cst = (nxt - pre) * P_COST[0] // P_COST[1]
		status = glb.get_YN(f'请确认是否加油：燃油量从 {pre} 加到 {nxt} 花费 {cst}')
		if not status:
			return
		self.dr.p = nxt
		self.dr.money -= cst

	def try_fillg(self):
		pre, nxt = self.dr.g, min(self.dr.g_max, self.dr.g + self.dr.money * G_COST[1] // G_COST[0])
		if pre == nxt and nxt != self.dr.g_max:
			glb.show_WN('没钱加气')
			return
		elif pre == nxt:
			glb.show_WN('无需加气', color = DARK_GREEN)
			return
		cst = (nxt - pre) * G_COST[0] // G_COST[1]
		status = glb.get_YN(f'请确认是否加气：氮气量从 {pre} 加到 {nxt} 花费 {cst}')
		if not status:
			return
		self.dr.g = nxt
		self.dr.money -= cst

	def try_repair(self):
		pre, nxt = self.dr.h, min(self.dr.h_max, self.dr.h + self.dr.money * R_COST[1] // R_COST[0])
		if pre == nxt and nxt != self.dr.h_max:
			glb.show_WN('没钱维修')
			return
		elif pre == nxt:
			glb.show_WN('无需维修', color = DARK_GREEN)
			return
		cst = (nxt - pre) * R_COST[0] // R_COST[1]
		status = glb.get_YN(f'请确认是否维修：血量从 {pre} 维修到 {nxt} 花费 {cst}')
		if not status:
			return
		self.dr.h = nxt
		self.dr.money -= cst

	def try_sell(self):
		money = 0
		for ore in self.dr.carry:
			money += get_val(ore) * self.dr.carry[ore]
			self.dr.carry[ore] = 0
		glb.show_WN(f'售出所有矿物，获得金钱 {money}')
		self.dr.money += money
		self.dr.o = 0
		glb.achieve.vals['tot-money'] += money
		self.ore.update()

	def try_move(self, d, speedup):
		nr, nc = self.dr.r + D_XY[d][0], self.dr.c + D_XY[d][1]
		if not self.mp.in_map(nr, nc):
			return
		if self.dr.r != 0 and nr != 0 and self.dr.p <= 0:
			return
		if (is_ore(self.mp.mp[nr][nc]) or is_dirt(self.mp.mp[nr][nc]) or is_chest(self.mp.mp[nr][nc])) and self.dr.h <= 0:
			return
		if self.dr.g <= 0:
			speedup = 0
		speed = get_speed_level(self.mp.mp[nr][nc], self.dr.rgd_l, self.dr.eng_l, speedup)
		if speed[0] == 0:
			return

		self.prepare_move(d, speedup, nr, nc, speed)

	def prepare_move(self, d, speedup, nr, nc, speed):
		if speedup:
			self.dr.g -= 1
			self.dr.g = max(self.dr.g, 0)
		self.nr, self.nc = nr, nc
		self.speed = speed
		self.mv_timer = self.speed[1]
		self.pixel = 0
		self.drill.is_moving = 1
		self.drill.speedup = speedup
		self.drill.dir = d
		if is_ore(self.mp.mp[nr][nc]) or is_dirt(self.mp.mp[nr][nc]) or is_chest(self.mp.mp[nr][nc]):
			self.drill.is_drilling = 1

	def move(self):
		if self.dr.r != 0 or self.nr != 0:
			self.dr.p -= 1
			self.dr.p = max(self.dr.p, 0)
		d, spd = self.drill.dir, 0
		self.mv_timer -= 1
		if self.mv_timer == 0:
			self.pixel += self.speed[0]
			spd = self.speed[0]
			self.mv_timer = self.speed[1]
		if spd == 0:
			return
		r, c = self.dr.r, self.dr.c
		nr, nc = self.nr, self.nc
		if d == D_D or d == D_U:
			if self.mp.in_bound_r(r) and self.mp.in_bound_r(nr):
				self.bg.move(D_MP[d], spd)
				self.map.move(D_MP[d], spd)
				self.mp.r = nr
			else:
				self.drill.move(BG_DIR_MP[d], spd)
		else:
			if self.mp.in_bound_c(c) and self.mp.in_bound_c(nc):
				self.bg.move(D_MP[d], spd)
				self.map.move(D_MP[d], spd)
				self.mp.c = nc
			else:
				self.drill.move(BG_DIR_MP[d], spd)
		if self.pixel == BLOCK_SZ:
			self.move_finish()

	def move_finish(self):
		self.dr.r, self.dr.c = self.nr, self.nc
		self.pixel = 0
		self.drill.is_moving = 0
		self.drill.is_drilling = 0

		r, c = self.nr, self.nc
		if is_dirt(self.mp.mp[r][c]):
			self.cover_dirt(self.mp.mp[r][c])
		if is_ore(self.mp.mp[r][c]):
			self.cover_ore(self.mp.mp[r][c])
		if is_chest(self.mp.mp[r][c]):
			self.cover_chest(self.mp.mp[r][c])
		if is_NPC(self.mp.mp[r][c]):
			self.cover_npc(self.mp.mp[r][c])
		glb.achieve.vals['tot-move'] += 1
		self.map.update_map(r, c)

	def cover_dirt(self, idx):
		glb.achieve.vals[idx] += 1
		glb.achieve.vals['tot-dirt'] += 1
		self.dr.h -= get_damage(idx)
		self.dr.h = max(self.dr.h, 0)

	def cover_ore(self, idx):
		glb.achieve.vals[idx] += 1
		glb.achieve.vals['tot-ore'] += 1
		self.ore.update(idx)
		if self.dr.o < self.dr.o_max:
			self.dr.o += 1
			self.dr.carry[idx] += 1
		self.dr.h -= get_damage(idx)
		self.dr.h = max(self.dr.h, 0)

	def cover_chest(self, idx):
		glb.achieve.vals[idx] += 1
		glb.achieve.vals['tot-chest'] += 1
		self.dr.money += get_val(idx)
		self.dr.h -= get_damage(idx)
		self.dr.h = max(self.dr.h, 0)

	def cover_npc(self, idx):
		glb.achieve.vals[idx] += 1
		glb.achieve.vals['tot-npc'] += 1
		self.mp.npc[idx] = 1

	def update_fps(self):
		self.frame_cnt += 1
		if self.frame_cnt == FPS // 4:
			now = datetime.now()
			diff = now - self.pre_time
			self.pre_time = now
			self.pre_fps = 1 / diff.total_seconds() * (FPS // 4)
			self.frame_cnt = 0

	def draw(self, scr):
		self.bg.draw(scr)
		self.map.draw(scr)
		self.drill.draw(scr)
		if self.show_info:
			self.info.draw(scr)
		if self.show_npc:
			self.npc.draw(scr)
		if self.show_ore:
			self.ore.draw(scr)
		if self.show_bar:
			self.bar.draw(scr)


TEXT_COLOR = (220, 220, 220)


class Text:
	def __init__(self):
		self.list = []

	def add(self, s, x = 0, y = 0, font = default_font, color = TEXT_COLOR, bold = False):
		if bold:
			font.bold = True
		text = font.render(s, True, color)
		if bold:
			font.bold = False
		rect = text.get_rect()
		rect.x = x
		rect.y = y
		self.list.append([text, rect])
		return rect

	def add_row(self, s, x = 0, gap = BLOCK_SZ, font = default_font, color = TEXT_COLOR, bold = False):
		if bold:
			font.bold = True
		text = font.render(s, True, color)
		if bold:
			font.bold = False
		rect = text.get_rect()
		rect.x = x
		if len(self.list) == 0:
			rect.y = 0
		else:
			rect.y = self.list[-1][1].y + gap
		self.list.append([text, rect])
		return rect

	def clear(self):
		self.list.clear()

	def draw(self, scr):
		for t, r in self.list:
			scr.blit(t, r)


GAME_INFO_LEN = 70


class Game_Info:
	def __init__(self, page: Page_Game):
		self.page = page
		self.bg = page.bg
		self.mp = page.mp
		self.dr = page.dr
		self.info = Text()

	def update(self, level = 0):
		self.info.clear()
		if level == 1:
			self.info.add_row(f'FPS: {int(self.page.pre_fps)}')
			return
		if level >= 2:
			self.info.add_row(f'FPS: {int(self.page.pre_fps)}, 屏幕大小: {SCR_N}行, {SCR_M}列, 地图大小:{self.mp.n}行, {self.mp.m}列')
		if level >= 3:
			self.info.add_row(f'共有 {self.bg.tree_num} 棵树, {self.bg.cloud_num} 朵云, {self.bg.bird_num}只鸟')
		if level >= 2:
			self.info.add_row(f'钻机位置: {self.dr.r}行, {self.dr.c}列, 屏幕中心位置: {self.mp.r}行, {self.mp.c}列, 钻机所处格子ID: {self.mp.mp[self.dr.r][self.dr.c]}')
		if level >= 3:
			self.info.add_row(f'钻头等级：{self.dr.rgd_l}, 装甲等级：{self.dr.h_l}, 燃油箱等级：{self.dr.p_l}, 氮气箱等级：{self.dr.g_l}，引擎等级：{self.dr.eng_l}')
			self.info.add_row(f'金钱：{self.dr.money}, 燃油量：{self.dr.p}, 氮气量：{self.dr.g}，矿石容量：{self.dr.o}，血量：{self.dr.h}')
			s = '携带矿物：'
			for ore in ORES:
				s += f'{get_name(ore)}: {self.dr.carry[ore]} '
				if len(s) > GAME_INFO_LEN:
					self.info.add_row(s)
					s = ''
			if s != '':
				self.info.add_row(s)
		if level >= 2:
			s = '当前在地面'
			if self.mp.in_under(self.dr.r, self.dr.c):
				s = '当前在地下'
			elif self.mp.in_cave(self.dr.r, self.dr.c):
				s = '当前在洞穴'
			elif self.mp.in_shop(P_SHOP, self.dr.r, self.dr.c):
				s = '当前在加油站'
			elif self.mp.in_shop(O_SHOP, self.dr.r, self.dr.c):
				s = '当前在售卖处'
			elif self.mp.in_shop(G_SHOP, self.dr.r, self.dr.c):
				s = '当前在加气站'
			elif self.mp.in_shop(R_SHOP, self.dr.r, self.dr.c):
				s = '当前在维修站'
			elif self.mp.in_shop(D_SHOP, self.dr.r, self.dr.c):
				s = '当前在装备站'
			self.info.add_row(s)
		if level >= 4:
			s = '已获救NPC：'
			for npc in NPCS:
				if self.mp.npc[npc]:
					s += f'{get_name(npc)} '
					if len(s) > GAME_INFO_LEN:
						self.info.add_row(s)
						s = '  '
			if s != '':
				self.info.add_row(s)
			s = '未获救NPC；'
			for npc in NPCS:
				if not self.mp.npc[npc]:
					s += f'{get_name(npc)} '
					if len(s) > GAME_INFO_LEN:
						self.info.add_row(s)
						s = '  '
			if s != '':
				self.info.add_row(s)
		if level >= 5:
			self.info.add_row(f'档案：', color = (255, 255, 0), bold = True)
			s = '  物块：'
			for dirt in DIRTS:
				s += f'{get_name(dirt)}: {glb.achieve.vals[dirt]} '
				if len(s) > GAME_INFO_LEN:
					self.info.add_row(s)
					s = '    '
			if s != '':
				self.info.add_row(s)
			s = '  矿物：'
			for ore in ORES:
				s += f'{get_name(ore)}: {glb.achieve.vals[ore]} '
				if len(s) > GAME_INFO_LEN:
					self.info.add_row(s)
					s = '    '
			if s != '':
				self.info.add_row(s)
			s = '  宝箱：'
			for chest in CHESTS:
				s += f'{get_name(chest)}: {glb.achieve.vals[chest]} '
				if len(s) > GAME_INFO_LEN:
					self.info.add_row(s)
					s = '    '
			if s != '':
				self.info.add_row(s)
			s = '  NPC：'
			for npc in NPCS:
				s += f'{get_name(npc)}: {glb.achieve.vals[npc]} '
				if len(s) > GAME_INFO_LEN:
					self.info.add_row(s)
					s = '    '
			if s != '':
				self.info.add_row(s)
			self.info.add_row(f'存档：', color = (255, 255, 0), bold = True)
			for i in range(1, 11, 2):
				s = f'  存档 {i}:' + glb.log.logs_info[i] + f'  存档 {i + 1}:' + glb.log.logs_info[i + 1]
				self.info.add_row(s)


	def draw(self, scr):
		self.info.draw(scr)

	def empty(self):
		self.info.clear()


def init_Page_Game():
	return Page_Game()


def init_game(log_id = 0):
	if log_id != 0:
		glb.pages.append(Page_Game(log_id))
	else:
		result = []
		init_thread = threading.Thread(target = lambda: result.append(init_Page_Game()))
		init_thread.start()

		# play cg

		init_thread.join()
		glb.pages.append(result[0])
		'''
		glb.pages.append(init_Page_Game())
		'''



