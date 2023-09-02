import pygame as pg
import logging
import random
import sys
import os

import pygame.display

pg.init()
FONT_SIZE = 20
default_font = pg.font.SysFont('kaiti', 20)
logging.basicConfig(format = "%(levelname)s: %(message)s", level = logging.DEBUG)


# 控制按键映射（添加控制修改三个地方，控制映射值，控制列表，按键到控制的映射）

# 空控制（用于表示没有触发任何控制的情况）
CTRL_NONE = 0
# 退出、回车
CTRL_ESC, CTRL_ENTER = 1000, -1000
CTRL_SH, CTRL_TAB = -20, -10
# 上、下、左、右、空格
CTRL_U, CTRL_D, CTRL_L, CTRL_R, CTRL_SP = 1, 2, 3, 4, 5
# 交互
CTRL_INTER = 10
# 用于使用键盘控制选项，使用 CTRL_OP[1~10] 表示选项 1~10
CTRL_OPT = [20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30]

# 此列表记录所有已知控制
CTRL_LIST = [
	CTRL_NONE,
	CTRL_ESC, CTRL_ENTER,
	CTRL_SH, CTRL_TAB,
	CTRL_U, CTRL_D, CTRL_L, CTRL_R, CTRL_SP,
	CTRL_INTER
]
CTRL_LIST = CTRL_LIST + CTRL_OPT

# 按键到控制的映射关系（可以有多个按键指向同一个控制）
KEY_TO_CTRL = {
	pg.K_ESCAPE: CTRL_ESC,
	pg.K_RETURN: CTRL_ENTER,
	pg.K_LSHIFT: CTRL_SH, pg.K_RSHIFT: CTRL_SH,
	pg.K_TAB: CTRL_TAB,
	pg.K_UP: CTRL_U, pg.K_w: CTRL_U,
	pg.K_DOWN: CTRL_D, pg.K_s: CTRL_D,
	pg.K_LEFT: CTRL_L, pg.K_a: CTRL_L,
	pg.K_RIGHT: CTRL_R, pg.K_d: CTRL_R,
	pg.K_SPACE: CTRL_SP,
	pg.K_e: CTRL_INTER, pg.K_f: CTRL_INTER,
	pg.K_1: CTRL_OPT[1],  pg.K_KP1: CTRL_OPT[1],  pg.K_KP_1: CTRL_OPT[1],
	pg.K_2: CTRL_OPT[2],  pg.K_KP2: CTRL_OPT[2],  pg.K_KP_2: CTRL_OPT[2],
	pg.K_3: CTRL_OPT[3],  pg.K_KP3: CTRL_OPT[3],  pg.K_KP_3: CTRL_OPT[3],
	pg.K_4: CTRL_OPT[4],  pg.K_KP4: CTRL_OPT[4],  pg.K_KP_4: CTRL_OPT[4],
	pg.K_5: CTRL_OPT[5],  pg.K_KP5: CTRL_OPT[5],  pg.K_KP_5: CTRL_OPT[5],
	pg.K_6: CTRL_OPT[6],  pg.K_KP6: CTRL_OPT[6],  pg.K_KP_6: CTRL_OPT[6],
	pg.K_7: CTRL_OPT[7],  pg.K_KP7: CTRL_OPT[7],  pg.K_KP_7: CTRL_OPT[7],
	pg.K_8: CTRL_OPT[8],  pg.K_KP8: CTRL_OPT[8],  pg.K_KP_8: CTRL_OPT[8],
	pg.K_9: CTRL_OPT[9],  pg.K_KP9: CTRL_OPT[9],  pg.K_KP_9: CTRL_OPT[9],
	pg.K_0: CTRL_OPT[10], pg.K_KP0: CTRL_OPT[10], pg.K_KP_0: CTRL_OPT[10]
}


# 方向映射

# 无方向、右、下、左、上
D_N, D_R, D_D, D_L, D_U = 0, 1, 2, 3, 4
# 方向对应的 dx、dy，D_XY[d][0] 为 dx，D_XY[d][1] 为 dy
D_XY = {D_N: [0, 0], D_R: [0, 1], D_D: [1, 0], D_L: [0, -1], D_U: [-1, 0]}
# 由地图坐标系转换为钻机坐标系的映射，同时也是钻机坐标系转换为地图坐标系的映射
D_MP = {D_N: D_N, D_U: D_R, D_D: D_L, D_L: D_D, D_R: D_U}

# 方向控制转换为方向的映射
CTRL_DIR = {CTRL_U: D_U, CTRL_D: D_D, CTRL_L: D_L, CTRL_R: D_R}


# 物块图片大小，以像素为单位，必须为加速系数的倍数
BLOCK_SZ = 24


# 屏幕信息
# 屏幕中每行、每列的物块数，必须为奇数
SCR_INFO = pygame.display.Info()
SCR_N, SCR_M = 45, 79
if SCR_INFO.current_h < 1440 or SCR_INFO.current_w < 2560:
	SCR_N, SCR_M = 37, 65
if SCR_INFO.current_h < 1080 or SCR_INFO.current_w < 1920:
	SCR_N, SCR_M = 29, 53
if SCR_INFO.current_h < 900 or SCR_INFO.current_w < 1600:
	SCR_N, SCR_M = 25, 41
# 屏幕中心点的物块坐标
SCR_CEN_R, SCR_CEN_C = SCR_N // 2 + 1, SCR_M // 2 + 1
# 屏幕大小
SCR_W = SCR_M * BLOCK_SZ
SCR_H = SCR_N * BLOCK_SZ
SCR_CEN_X, SCR_CEN_Y = SCR_W // 2, SCR_H // 2
# 刷新率
FPS = 48


# 地图相关常量
# 空物块
EMPTY = 0
# 土块
DIRT = 1
# 矿物
COAL, COPPER, SILVER, GOLD, AMETHYST, EMERALD, SAPPHIRE, RUBY, DIAMOND = 2, 3, 4, 5, 6, 7, 8, 9, 10
# 路面
ROAD = 20

# 矿物参数常量
ORE_DENSITY_SIZE = 40000    # 密度计算公式 num//DENSITY_SIZE
ORES = [COAL, COPPER, SILVER, GOLD, AMETHYST, EMERALD, SAPPHIRE, RUBY, DIAMOND]
ORES_TOT = len(ORES)

BLK_DATA = {
	DIRT:      {'name': '土块',   'rgd': 1},
	COAL:      {'name': '煤矿',   'rgd': 2,  'sz': 19, 'num': 50, 'layer': 1, 'grow': 1, 'min_sz': 1},
	COPPER:    {'name': '铜矿',   'rgd': 3,  'sz': 16, 'num': 45, 'layer': 1, 'grow': 1, 'min_sz': 1},
	SILVER:    {'name': '银矿',   'rgd': 4,  'sz': 14, 'num': 40, 'layer': 1, 'grow': 1, 'min_sz': 1},
	GOLD:      {'name': '金矿',   'rgd': 5,  'sz': 12, 'num': 35, 'layer': 1, 'grow': 1, 'min_sz': 1},
	AMETHYST:  {'name': '紫晶',   'rgd': 6,  'sz': 9,  'num': 30, 'layer': 1, 'grow': 1, 'min_sz': 1},
	EMERALD:   {'name': '翡翠',   'rgd': 7,  'sz': 8,  'num': 25, 'layer': 1, 'grow': 1, 'min_sz': 1},
	SAPPHIRE:  {'name': '蓝宝石', 'rgd': 8,  'sz': 6,  'num': 20, 'layer': 1, 'grow': 1, 'min_sz': 1},
	RUBY:      {'name': '红宝石', 'rgd': 9,  'sz': 4,  'num': 15, 'layer': 1, 'grow': 1, 'min_sz': 1},
	DIAMOND:   {'name': '钻石',   'rgd': 10, 'sz': 3,  'num': 10, 'layer': 1, 'grow': 1, 'min_sz': 1}
}

ORES_VALUE = {
	COAL: 100,
	COPPER: 200,
	SILVER: 300,
	GOLD: 400,
	AMETHYST: 500,
	EMERALD: 600,
	SAPPHIRE: 700,
	RUBY: 800,
	DIAMOND: 1000
}

# 矿物默认参数
ORES_SIZE_K = [3, 3, 3, 3, 3, 3, 3, 3, 3]
ORES_NUM_K = [3, 3, 3, 3, 3, 3, 3, 3, 3]
ORES_LAYER_K = [3, 3, 3, 3, 3, 3, 3, 3, 3]
ORES_GROW_K = [3, 3, 3, 3, 3, 3, 3, 3, 3]
ORES_MIN_SZ_K = [3, 3, 3, 3, 3, 3, 3, 3, 3]

for i in range(0, ORES_TOT):
	ore = ORES[i]
	BLK_DATA[ore]['sz'] *= ORES_SIZE_K[i]
	BLK_DATA[ore]['num'] *= ORES_NUM_K[i]
	BLK_DATA[ore]['layer'] *= ORES_LAYER_K[i]
	BLK_DATA[ore]['grow'] *= ORES_GROW_K[i]
	BLK_DATA[ore]['min_sz'] *= ORES_MIN_SZ_K[i]

# 地图默认行、列数，必须为奇数
MAP_N, MAP_M = 201, 301
# 矿物生成缓冲区高度
EMPTY_LAYER_H = 10

BLK_IMG_URL = {
	DIRT: './assets/img/block/dirt.png',
	COAL: './assets/img/block/coal.png',
	COPPER: './assets/img/block/copper.png',
	SILVER: './assets/img/block/silver.png',
	GOLD: './assets/img/block/gold.png',
	AMETHYST: './assets/img/block/amethyst.png',
	EMERALD: './assets/img/block/emerald.png',
	SAPPHIRE: './assets/img/block/sapphire.png',
	RUBY: './assets/img/block/ruby.png',
	DIAMOND: './assets/img/block/diamond.png',
	ROAD: './assets/img/block/road.png',
}


# 背景相关常量
SKY, EMPTY_BG = 1, 2
CLOUD, CLOUD_LEN = 10, 5
TREE, TREE_LEN = 20, 5
PETROL_SHOP, GAS_SHOP, ORES_SHOP, DRILL_SHOP = 30, 40, 50, 60
COVER = 100

# 云层信息
# 云层移动速度和方向
CLOUD_SP = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
CLOUD_DIR = [D_D, D_U]
# 云层默认数量
CLOUD_GEN_SPEED = 1
CLOUD_NUM_MAX = 10
CLOUD_DENSITY_SIZE = 2500

# 树木信息
TREE_NUM_MAX = 10
TREE_DENSITY_LEN = 300

SHOP_N = {
	PETROL_SHOP: 4,
	GAS_SHOP: 4,
	ORES_SHOP: 4,
	DRILL_SHOP: 4,
}
SHOP_W = {
	PETROL_SHOP: 4,
	GAS_SHOP: 4,
	ORES_SHOP: 4,
	DRILL_SHOP: 4
}
SHOP_POS = {
	PETROL_SHOP: -5,
	GAS_SHOP: -10,
	ORES_SHOP: 2,
	DRILL_SHOP: 7,
}

PETROL_COST = 1
GAS_COST = 1

BG_IMG_URL = {
	EMPTY_BG: './assets/img/bg/empty.png',
	SKY: './assets/img/bg/sky.png',
	CLOUD: './assets/img/bg/cloud_{}_{}.png',
	TREE: './assets/img/bg/tree_{}_{}.png',
	PETROL_SHOP: './assets/img/bg/petrol-shop_{}.png',
	GAS_SHOP: './assets/img/bg/gas-shop_{}.png',
	ORES_SHOP: './assets/img/bg/ores-shop_{}.png',
	DRILL_SHOP: './assets/img/bg/drill-shop_{}.png',
	COVER: './assets/img/bg/cover.png',
}


# 钻机物品 ID
BODY, HEAD = 10, 20
SFLAME, LFLAME = 30, 40

DRILL_LEVEL_MAX = 5
DRILL_DATA = {
	'rgd':   [2, 4, 6, 8, 9, 10],
	'eng':   [10, 1, 2, 3, 4, 5],
	'p_cap': [10000, 15000, 20000, 30000, 50000, 100000],
	'g_cap': [100, 110, 120, 130, 140, 150],
	'o_cap': [40, 50, 60, 70, 80, 90]
}

DRILL_COST = {
	'rgd':   [100, 200, 300, 400, 500],
	'eng':   [100, 200, 300, 400, 500],
	'p_cap': [100, 200, 300, 400, 500],
	'g_cap': [100, 200, 300, 400, 500],
	'o_cap': [100, 200, 300, 400, 500]
}

# 钻机参数常量
SPEED_LEVEL = [
	[[0, -1], [1, 4], [1, 3], [1, 2], [1, 1], [2, 1], [3, 1], [4, 1], [6,  1], [12, 1]],
	[[0, -1], [1, 2], [2, 3], [1, 1], [2, 1], [4, 1], [6, 1], [8, 1], [12, 1], [24, 1]]
]
SPEED_LEVEL_TOT = len(SPEED_LEVEL[0])

DR_IMG_URL = {
	BODY:   './assets/img/drill/body_{}_{}_{}.png',
	HEAD:   './assets/img/drill/head_{}_{}_{}.png',
	SFLAME: './assets/img/drill/sflame_{}_{}_{}.png',
	LFLAME: './assets/img/drill/lflame_{}_{}_{}.png',
}


# 页面常量
PAGE_NONE = 0
PAGE_EXIT = -1

P_ACHIEVE, P_INFO, P_KEYS, P_MENU, P_PAUSE, P_READ, P_SAVE, P_YN, P_SHOP, P_OVER = 1, 2, 3, 4, 5, 6, 7, 8, 9, 10

PAGE_URL = {
	P_ACHIEVE: './assets/img/page/achieve.png',
	P_INFO:    './assets/img/page/info.png',
	P_KEYS:    './assets/img/page/keys.png',
	P_MENU:    './assets/img/page/menu.png',
	P_PAUSE:   './assets/img/page/pause.png',
	P_READ:    './assets/img/page/read.png',
	P_SAVE:    './assets/img/page/save.png',
	P_YN:      './assets/img/page/YN.png',
	P_SHOP:    './assets/img/page/shop.png',
	P_OVER:    './assets/img/page/over.png',
}


LOG_NUM_MAX = 10
LOG_ROOT_URL = './.log'
LOG_EMPTY_INFO = '空存档'
LOG_INFO_FORM = '存档时间：{}'

if not os.path.exists(LOG_ROOT_URL):
	os.mkdir(LOG_ROOT_URL)

IMG_ROLL_SP = 48


ACHIEVE_URL = './achieve'
ACHIEVE_DEFAULT = {
	DIRT: 0,
	COAL: 0,
	COPPER: 0,
	SILVER: 0,
	GOLD: 0,
	AMETHYST: 0,
	EMERALD: 0,
	SAPPHIRE: 0,
	RUBY: 0,
	DIAMOND: 0,
	'tot_ore': 0,
	'tot_move': 0,
	'tot_money': 0
}

if not os.path.exists(ACHIEVE_URL):
	open(ACHIEVE_URL, mode = 'w')
