import pygame as PG
import logging
import random
import sys
import os


logging.basicConfig(format = "%(levelname)s: %(message)s", level = logging.DEBUG)


# 控制按键映射（添加控制修改三个地方，控制映射值，控制列表，按键到控制的映射）

# 空控制（用于表示没有触发任何控制的情况）
CTRL_NONE = 0
# 退出、回车
CTRL_ESC, CTRL_ENTER = 1000, -1000
CTRL_TAB, CTRL_SH = -10, -20
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
	CTRL_TAB, CTRL_SH,
	CTRL_U, CTRL_D, CTRL_L, CTRL_R, CTRL_SP,
	CTRL_INTER
]
CTRL_LIST = CTRL_LIST+CTRL_OPT

# 按键到控制的映射关系（可以有多个按键指向同一个控制）
KEY_TO_CTRL = {
	PG.K_ESCAPE: CTRL_ESC,
	PG.K_RETURN: CTRL_ENTER,
	PG.K_LSHIFT: CTRL_SH,
	PG.K_UP: CTRL_U, PG.K_w: CTRL_U,
	PG.K_DOWN: CTRL_D, PG.K_s: CTRL_D,
	PG.K_LEFT: CTRL_L, PG.K_a: CTRL_L,
	PG.K_RIGHT: CTRL_R, PG.K_d: CTRL_R,
	PG.K_SPACE: CTRL_SP,
	PG.K_e: CTRL_INTER,
	PG.K_1: CTRL_OPT[1],
	PG.K_2: CTRL_OPT[2],
	PG.K_3: CTRL_OPT[3],
	PG.K_4: CTRL_OPT[4],
	PG.K_5: CTRL_OPT[5],
	PG.K_6: CTRL_OPT[6],
	PG.K_7: CTRL_OPT[7],
	PG.K_8: CTRL_OPT[8],
	PG.K_9: CTRL_OPT[9],
	PG.K_0: CTRL_OPT[10],
	PG.K_KP1: CTRL_OPT[1],
	PG.K_KP2: CTRL_OPT[2],
	PG.K_KP3: CTRL_OPT[3],
	PG.K_KP4: CTRL_OPT[4],
	PG.K_KP5: CTRL_OPT[5],
	PG.K_KP6: CTRL_OPT[6],
	PG.K_KP7: CTRL_OPT[7],
	PG.K_KP8: CTRL_OPT[8],
	PG.K_KP9: CTRL_OPT[9],
	PG.K_KP0: CTRL_OPT[10],
	PG.K_KP_1: CTRL_OPT[1],
	PG.K_KP_2: CTRL_OPT[2],
	PG.K_KP_3: CTRL_OPT[3],
	PG.K_KP_4: CTRL_OPT[4],
	PG.K_KP_5: CTRL_OPT[5],
	PG.K_KP_6: CTRL_OPT[6],
	PG.K_KP_7: CTRL_OPT[7],
	PG.K_KP_8: CTRL_OPT[8],
	PG.K_KP_9: CTRL_OPT[9],
	PG.K_KP_0: CTRL_OPT[10],
}


# 方向映射

# 无方向、右、下、左、上
D_N, D_R, D_D, D_L, D_U = 0, 1, 2, -1, -2
# 方向对应的 dx、dy，D_XY[d][0] 为 dx，D_XY[d][1] 为 dy
D_XY = {D_N: [0, 0], D_R: [0, 1], D_D: [1, 0], D_L: [0, -1], D_U: [-1, 0]}
# 由地图坐标系转换为钻机坐标系的映射，同时也是钻机坐标系转换为地图坐标系的映射
D_MP = {D_N: D_N, D_U: D_R, D_D: D_L, D_L: D_D, D_R: D_U}

# 方向控制转换为方向的映射
CTRL_DIR = {CTRL_U: D_U, CTRL_D: D_D, CTRL_L: D_L, CTRL_R: D_R}


# 物块图片大小，以像素为单位，必须为加速系数的倍数
BLOCK_SZ = 24


# 移动速度
SPEED_LEVEL = [
	[[0, -1], [1, 4], [1, 3], [1, 2], [1, 1], [2, 1], [3, 1], [4, 1], [6, 1], [12, 1]],
	[[0, -1], [1, 2], [2, 3], [1, 1], [2, 1], [4, 1], [6, 1], [8, 1], [12, 1], [24, 1]]
]
SPEED_LEVEL_TOT = len(SPEED_LEVEL)

# 云层信息
# 云层移动速度和方向
CLOUD_SP = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
CLOUD_DIR = [D_L, D_R]
# 云层默认数量
CLOUD_NUM = 10
CLOUD_DENSITY_SIZE = 2500


# 树木信息
TREE_NUM = 10
TREE_DENSITY_SIZE = 100


# 屏幕信息

# 屏幕中每行、每列的物块数，必须为奇数
SCR_N, SCR_M = 39, 55
# 屏幕中心点的物块坐标
SCR_CEN_R, SCR_CEN_C = SCR_N // 2 + 1, SCR_M // 2 + 1
# 屏幕大小
SCR_W = SCR_M * BLOCK_SZ
SCR_H = SCR_N * BLOCK_SZ
SCR_CEN_X, SCR_CEN_Y = SCR_W // 2 + 1, SCR_H // 2 + 1
# 刷新率
FPS = 48


# 物块物品 ID

# 空物块
EMPTY = 0
# 土块
DIRT = 1
# 矿物
COAL, COPPER, SILVER, GOLD, AMETHYST = 2, 3, 4, 5, 6
EMERALD, SAPPHIRE, RUBY, DIAMOND = 7, 8, 9, 10


# 背景物品 ID
ROAD = -1
EMPTY_BG = -100
SKY = -50
CLOUDS = [-40, -41, -42, -43, -44]
TREES = [-30, -31, -32, -33, -34]
PETROL_STATION, GAS_STATION = -20, -25
DRILL_SHOP, WEAPON_SHOP = -10, -15
REPAIR_SHOP = -5
COVER = 1000

# 钻机物品 ID
D_BODYS = [30, 31, 32, 33, 34]
D_HEADS = [40, 41, 42, 43, 44]
D_S_FLAMES = [50, 51, 52, 53, 54]
D_L_FLAMES = [60, 61, 62, 63, 64]


# 矿物参数常量
DENSITY_SIZE = 40000    # 密度计算公式 num//DENSITY_SIZE
ORES = [COAL, COPPER, SILVER, GOLD, AMETHYST, EMERALD, SAPPHIRE, RUBY, DIAMOND]
ORES_K = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]    # [0] 为默认值
ORES_TOT = len(ORES)

DIRT_DATA = {'name': '土块', 'rgd': 1}
ORES_DATA = {
	COAL:      {'name': '煤矿',   'rgd': 2,  'sz': 19, 'num': 50, 'layer': 1, 'grow': 1, 'min_sz': 1},
	COPPER:    {'name': '铜矿',   'rgd': 3,  'sz': 16, 'num': 45, 'layer': 1, 'grow': 1, 'min_sz': 1},
	SILVER:    {'name': '银矿',   'rgd': 4,  'sz': 14, 'num': 40, 'layer': 1, 'grow': 1, 'min_sz': 1},
	GOLD:      {'name': '金矿',   'rgd': 5,  'sz': 12, 'num': 35, 'layer': 1, 'grow': 1, 'min_sz': 1},
	AMETHYST:  {'name': '紫晶',   'rgd': 6,  'sz': 9,  'num': 30, 'layer': 1, 'grow': 1, 'min_sz': 1},
	EMERALD:   {'name': '翡翠',   'rgd': 7,  'sz': 8,  'num': 25, 'layer': 1, 'grow': 1, 'min_sz': 1},
	SAPPHIRE:  {'name': '蓝宝石', 'rgd': 8,  'sz': 6,  'num': 20, 'layer': 1, 'grow': 1, 'min_sz': 1},
	RUBY:      {'name': '红宝石', 'rgd': 9,  'sz': 4,  'num': 15, 'layer': 1, 'grow': 1, 'min_sz': 1},
	DIAMOND:   {'name': '钻石',   'rgd': 10, 'sz': 3,  'num': 10, 'layer': 1, 'grow': 1, 'min_sz': 1},
}

# 矿物默认参数
ORES_SIZE_K = [3, 3, 3, 3, 3, 3, 3, 3, 3]
ORES_NUM_K = [3, 3, 3, 3, 3, 3, 3, 3, 3]
ORES_LAYER_K = [3, 3, 3, 3, 3, 3, 3, 3, 3]
ORES_GROW_K = [3, 3, 3, 3, 3, 3, 3, 3, 3]
ORES_MIN_SZ_K = [3, 3, 3, 3, 3, 3, 3, 3, 3]


DRILL_DATA = {
	0: {'rgd': 5}
}

# 地图默认行、列数，必须为奇数
MAP_N, MAP_M = 101, 201
# 矿物生成缓冲区高度
EMPTY_LAYER_H = 10


# 界面动作常量
PAGE_NONE = 0
PAGE_EXIT = -1


# 物品图片信息
IMG_URL = {
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
	EMPTY_BG: './assets/img/bg/empty.png',
	SKY: './assets/img/bg/sky.png',
	CLOUDS[0]: './assets/img/bg/cloud-0_{}.png',
	CLOUDS[1]: './assets/img/bg/cloud-1_{}.png',
	CLOUDS[2]: './assets/img/bg/cloud-2_{}.png',
	CLOUDS[3]: './assets/img/bg/cloud-3_{}.png',
	CLOUDS[4]: './assets/img/bg/cloud-4_{}.png',
	TREES[0]: './assets/img/bg/tree-0_{}.png',
	TREES[1]: './assets/img/bg/tree-1_{}.png',
	TREES[2]: './assets/img/bg/tree-2_{}.png',
	TREES[3]: './assets/img/bg/tree-3_{}.png',
	TREES[4]: './assets/img/bg/tree-4_{}.png',
	PETROL_STATION: './assets/img/bg/petrol-station_{}.png',
	GAS_STATION: './assets/img/bg/gas-station_{}.png',
	DRILL_SHOP: './assets/img/bg/drill-shop_{}.png',
	WEAPON_SHOP: './assets/img/bg/weapon-shop_{}.png',
	REPAIR_SHOP: './assets/img/bg/repair-shop_{}.png',
	COVER: './assets/img/bg/cover.png',
	D_BODYS[0]: './assets/img/drill/body-0_{}.png',
	D_BODYS[1]: './assets/img/drill/body-1_{}.png',
	D_BODYS[2]: './assets/img/drill/body-2_{}.png',
	D_BODYS[3]: './assets/img/drill/body-3_{}.png',
	D_BODYS[4]: './assets/img/drill/body-4_{}.png',
	D_HEADS[0]: './assets/img/drill/head-0_{}.png',
	D_HEADS[1]: './assets/img/drill/head-1_{}.png',
	D_HEADS[2]: './assets/img/drill/head-2_{}.png',
	D_HEADS[3]: './assets/img/drill/head-3_{}.png',
	D_HEADS[4]: './assets/img/drill/head-4_{}.png',
	D_S_FLAMES[0]: './assets/img/drill/small-flame-0_{}.png',
	D_S_FLAMES[1]: './assets/img/drill/small-flame-1_{}.png',
	D_S_FLAMES[2]: './assets/img/drill/small-flame-2_{}.png',
	D_S_FLAMES[3]: './assets/img/drill/small-flame-3_{}.png',
	D_S_FLAMES[4]: './assets/img/drill/small-flame-4_{}.png',
	D_L_FLAMES[0]: './assets/img/drill/large-flame-0_{}.png',
	D_L_FLAMES[1]: './assets/img/drill/large-flame-1_{}.png',
	D_L_FLAMES[2]: './assets/img/drill/large-flame-2_{}.png',
	D_L_FLAMES[3]: './assets/img/drill/large-flame-3_{}.png',
	D_L_FLAMES[4]: './assets/img/drill/large-flame-4_{}.png',
}

IMG_ROLL = {
	CLOUDS[0]: 15,
	CLOUDS[1]: 15,
	CLOUDS[2]: 15,
	CLOUDS[3]: 15,
	CLOUDS[4]: 15,
	TREES[0]: 15,
	TREES[1]: 15,
	TREES[2]: 15,
	TREES[3]: 15,
	TREES[4]: 15,
	D_BODYS[0]: 15,
	D_BODYS[1]: 15,
	D_BODYS[2]: 15,
	D_BODYS[3]: 15,
	D_BODYS[4]: 15,
}
