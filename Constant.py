import pygame as pg
import logging
import os
import imageio
from PIL import Image

pg.init()
logging.basicConfig(format = "%(levelname)s: %(message)s", level = logging.DEBUG)

# 控制按键映射（添加控制修改三个地方，控制映射值，控制列表，按键到控制的映射）
# 空控制（用于表示没有触发任何控制的情况）
CTRL_NONE = 0  # 不可变
# 退出（返回，取消）、确认（交互）、加速、详细信息
CTRL_ESC, CTRL_ENTER, CTRL_SH, CTRL_TAB = 1000, -1000, -20, -10
# 上、下、左、右    不可变
CTRL_R, CTRL_D, CTRL_L, CTRL_U = 1, 2, 3, 4
# I, J, K
CTRL_I, CTRL_J, CTRL_K = 10, 11, 12
# 用于使用键盘控制选项，使用 CTRL_OP[1~10] 表示选项 1~10
CTRL_OPT = [20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30]
CTRL_INTER = [40, 41, 42]

# 此列表记录所有已知控制
CTRL_LIST = [
	CTRL_NONE,
	CTRL_ESC, CTRL_ENTER, CTRL_SH, CTRL_TAB,
	CTRL_U, CTRL_D, CTRL_L, CTRL_R,
	CTRL_I, CTRL_J, CTRL_K
]
CTRL_LIST = CTRL_LIST + CTRL_OPT
CTRL_LIST = CTRL_LIST + CTRL_INTER

# 按键到控制的映射关系（可以有多个按键指向同一个控制）
KEY_TO_CTRL = {
	pg.K_ESCAPE: CTRL_ESC,
	pg.K_RETURN: CTRL_ENTER, pg.K_SPACE: CTRL_ENTER,
	pg.K_LSHIFT: CTRL_SH, pg.K_RSHIFT: CTRL_SH,
	pg.K_TAB: CTRL_TAB,
	pg.K_UP: CTRL_U, pg.K_w: CTRL_U,
	pg.K_DOWN: CTRL_D, pg.K_s: CTRL_D,
	pg.K_LEFT: CTRL_L, pg.K_a: CTRL_L,
	pg.K_RIGHT: CTRL_R, pg.K_d: CTRL_R,
	pg.K_i: CTRL_I,
	pg.K_j: CTRL_J,
	pg.K_k: CTRL_K,
	pg.K_1: CTRL_OPT[1], pg.K_KP1: CTRL_OPT[1], pg.K_KP_1: CTRL_OPT[1],
	pg.K_2: CTRL_OPT[2], pg.K_KP2: CTRL_OPT[2], pg.K_KP_2: CTRL_OPT[2],
	pg.K_3: CTRL_OPT[3], pg.K_KP3: CTRL_OPT[3], pg.K_KP_3: CTRL_OPT[3],
	pg.K_4: CTRL_OPT[4], pg.K_KP4: CTRL_OPT[4], pg.K_KP_4: CTRL_OPT[4],
	pg.K_5: CTRL_OPT[5], pg.K_KP5: CTRL_OPT[5], pg.K_KP_5: CTRL_OPT[5],
	pg.K_6: CTRL_OPT[6], pg.K_KP6: CTRL_OPT[6], pg.K_KP_6: CTRL_OPT[6],
	pg.K_7: CTRL_OPT[7], pg.K_KP7: CTRL_OPT[7], pg.K_KP_7: CTRL_OPT[7],
	pg.K_8: CTRL_OPT[8], pg.K_KP8: CTRL_OPT[8], pg.K_KP_8: CTRL_OPT[8],
	pg.K_9: CTRL_OPT[9], pg.K_KP9: CTRL_OPT[9], pg.K_KP_9: CTRL_OPT[9],
	pg.K_0: CTRL_OPT[10], pg.K_KP0: CTRL_OPT[10], pg.K_KP_0: CTRL_OPT[10],
	pg.K_e: CTRL_INTER[1],
	pg.K_f: CTRL_INTER[2]
}

# 方向映射
# 无方向、右、下、左、上    不可变
D_N, D_R, D_D, D_L, D_U = 0, 1, 2, 3, 4
# 方向对应的 dx、dy，D_XY[d][0] 为 dx，D_XY[d][1] 为 dy
D_XY = {D_N: [0, 0], D_R: [0, 1], D_D: [1, 0], D_L: [0, -1], D_U: [-1, 0]}
# 由地图坐标系转换为钻机坐标系的映射，同时也是钻机坐标系转换为地图坐标系的映射
D_MP = {D_N: D_N, D_U: D_R, D_D: D_L, D_L: D_D, D_R: D_U}

# 物块图片大小    不可变
BLOCK_SZ = 24

# 屏幕信息
# 屏幕中每行、每列的物块数    根据用户屏幕大小自适应
# 最大为 45 x 79 (1080, 1896)    最小为 25 x 41 (600, 984)
SCR_INFO = pg.display.Info()
SCR_N, SCR_M = 45, 79
if SCR_INFO.current_h < 1440 or SCR_INFO.current_w < 2560:
	SCR_N, SCR_M = 37, 65
if SCR_INFO.current_h < 1080 or SCR_INFO.current_w < 1920:
	SCR_N, SCR_M = 29, 53
if SCR_INFO.current_h < 900 or SCR_INFO.current_w < 1600:
	SCR_N, SCR_M = 25, 45
# 屏幕中心点的物块坐标
SCR_CEN_R, SCR_CEN_C = SCR_N // 2 + 1, SCR_M // 2 + 1
# 屏幕大小
SCR_W, SCR_H = SCR_M * BLOCK_SZ, SCR_N * BLOCK_SZ
# 屏幕中心 4 个像素点的左上角点坐标
SCR_CEN_X, SCR_CEN_Y = SCR_W // 2, SCR_H // 2
# 刷新率
FPS = 48
# 动态图片滚动速度
IMG_ROLL_SPD = 48
# 预加载行列数
PRE_LOAD = 1

# 地图相关常量
# 地图默认行、列数，必须为奇数
MAP_N, MAP_M = 101, 101

# 空物块
EMPTY = 0
# 阻挡物块（挖掉之后不会获得价值）
DIRTS = [1, 2, 3, 4, 5, 6, 7]
DIRT_TOT = len(DIRTS)
# 矿物物块（挖掉之后获得矿物）
ORES = [11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31]
ORE_TOT = len(ORES)
# 宝箱物块（挖掉之后立刻获得金钱）
CHESTS = [41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57]
CHEST_TOT = len(CHESTS)
# NPC物块（接触之后解救 NPC）
NPCS = [61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83]
NPC_TOT = len(NPCS)
# 迷雾物块
FOG = 90

# 矿物参数常量
BLK_DENS_SIZE = 50000  # 密度计算公式 num//DENSITY_SIZE
FOG_RAD = 5
BLK_DATA = {
	DIRTS[0]: {'name': '土块', 'rgd': 1, 'val': 0},
	DIRTS[1]: {'name': '粘土块', 'rgd': 4, 'val': 0},
	DIRTS[2]: {'name': '泥块', 'rgd': 7, 'val': 0},
	DIRTS[3]: {'name': '石块', 'rgd': 10, 'val': 0},
	DIRTS[4]: {'name': '黑檀石块', 'rgd': 13, 'val': 0},
	DIRTS[5]: {'name': '猩红石块', 'rgd': 16, 'val': 0},
	DIRTS[6]: {'name': '珍珠石块', 'rgd': 19, 'val': 0},
	ORES[0]: {'name': '铜矿', 'rgd': 2, 'sz': 30, 'num': 50, 'val': 10},
	ORES[1]: {'name': '锡矿', 'rgd': 3, 'sz': 30, 'num': 49, 'val': 20},
	ORES[2]: {'name': '铁矿', 'rgd': 4, 'sz': 30, 'num': 48, 'val': 30},
	ORES[3]: {'name': '铅矿', 'rgd': 5, 'sz': 28, 'num': 47, 'val': 40},
	ORES[4]: {'name': '银矿', 'rgd': 6, 'sz': 28, 'num': 46, 'val': 50},
	ORES[5]: {'name': '钨矿', 'rgd': 7, 'sz': 28, 'num': 45, 'val': 60},
	ORES[6]: {'name': '金矿', 'rgd': 8, 'sz': 26, 'num': 44, 'val': 70},
	ORES[7]: {'name': '铂金矿', 'rgd': 9, 'sz': 26, 'num': 43, 'val': 80},
	ORES[8]: {'name': '魔矿', 'rgd': 10, 'sz': 26, 'num': 42, 'val': 90},
	ORES[9]: {'name': '猩红矿', 'rgd': 11, 'sz': 24, 'num': 41, 'val': 100},
	ORES[10]: {'name': '陨石', 'rgd': 12, 'sz': 24, 'num': 40, 'val': 110},
	ORES[11]: {'name': '黑曜石', 'rgd': 13, 'sz': 24, 'num': 39, 'val': 120},
	ORES[12]: {'name': '狱石', 'rgd': 14, 'sz': 22, 'num': 38, 'val': 130},
	ORES[13]: {'name': '钴矿', 'rgd': 15, 'sz': 22, 'num': 37, 'val': 140},
	ORES[14]: {'name': '钯金矿', 'rgd': 16, 'sz': 22, 'num': 36, 'val': 150},
	ORES[15]: {'name': '秘银矿', 'rgd': 17, 'sz': 20, 'num': 35, 'val': 160},
	ORES[16]: {'name': '山铜矿', 'rgd': 18, 'sz': 20, 'num': 34, 'val': 170},
	ORES[17]: {'name': '精金矿', 'rgd': 19, 'sz': 20, 'num': 33, 'val': 180},
	ORES[18]: {'name': '钛金矿', 'rgd': 20, 'sz': 18, 'num': 32, 'val': 190},
	ORES[19]: {'name': '叶绿矿', 'rgd': 21, 'sz': 18, 'num': 31, 'val': 200},
	ORES[20]: {'name': '夜明矿', 'rgd': 22, 'sz': 18, 'num': 30, 'val': 210},
	CHESTS[0]: {'name': '木箱', 'rgd': 1, 'num': 30, 'val': 100},
	CHESTS[1]: {'name': '金箱', 'rgd': 2, 'num': 29, 'val': 200},
	CHESTS[2]: {'name': '冰冻箱', 'rgd': 3, 'num': 28, 'val': 300},
	CHESTS[3]: {'name': '红木箱', 'rgd': 5, 'num': 27, 'val': 400},
	CHESTS[4]: {'name': '砂岩箱', 'rgd': 7, 'num': 26, 'val': 500},
	CHESTS[5]: {'name': '水中箱', 'rgd': 9, 'num': 25, 'val': 600},
	CHESTS[6]: {'name': '暗影箱', 'rgd': 10, 'num': 24, 'val': 700},
	CHESTS[7]: {'name': '天域箱', 'rgd': 11, 'num': 23, 'val': 800},
	CHESTS[8]: {'name': '花岗岩箱', 'rgd': 12, 'num': 22, 'val': 900},
	CHESTS[9]: {'name': '大理石箱', 'rgd': 13, 'num': 21, 'val': 1000},
	CHESTS[10]: {'name': '黄金箱', 'rgd': 14, 'num': 20, 'val': 1100},
	CHESTS[11]: {'name': '腐化箱', 'rgd': 15, 'num': 19, 'val': 1200},
	CHESTS[12]: {'name': '猩红箱', 'rgd': 16, 'num': 18, 'val': 1300},
	CHESTS[13]: {'name': '神圣箱', 'rgd': 17, 'num': 17, 'val': 1400},
	CHESTS[14]: {'name': '冰冻箱', 'rgd': 18, 'num': 16, 'val': 1500},
	CHESTS[15]: {'name': '丛林箱', 'rgd': 19, 'num': 15, 'val': 1600},
	CHESTS[16]: {'name': '沙漠箱', 'rgd': 20, 'num': 14, 'val': 1700},
	NPCS[0]: {'name': '圣诞老人'},
	NPCS[1]: {'name': '护士'},
	NPCS[2]: {'name': '树妖'},
	NPCS[3]: {'name': '发型师'},
	NPCS[4]: {'name': '机械师'},
	NPCS[5]: {'name': '派对女孩'},
	NPCS[6]: {'name': '蒸汽朋克人'},
	NPCS[7]: {'name': '公主'},
	NPCS[8]: {'name': '巫师'},
	NPCS[9]: {'name': '军火商'},
	NPCS[10]: {'name': '动物学家'},
	NPCS[11]: {'name': '商人'},
	NPCS[12]: {'name': '机器侠'},
	NPCS[13]: {'name': '税收官'},
	NPCS[14]: {'name': '松露人'},
	NPCS[15]: {'name': '海盗'},
	NPCS[16]: {'name': '爆破专家'},
	NPCS[17]: {'name': '染料商'},
	NPCS[18]: {'name': '油漆工'},
	NPCS[19]: {'name': '高尔夫球手'},
	NPCS[20]: {'name': '酒馆老板'},
	NPCS[21]: {'name': '巫医'},
	NPCS[22]: {'name': '服装商'},
}

# 矿物可调系数
ORE_SZ_K = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
ORE_NUM_K = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
ORE_VAL_K = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
ORE_MINSZ_K = [50, 100]
ORE_GROW_K = [30, 100]
CHEST_NUM_K = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
CHEST_VAL_K = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]

for i in range(0, ORE_TOT):
	ore = ORES[i]
	BLK_DATA[ore]['sz'] *= ORE_SZ_K[i]
	BLK_DATA[ore]['num'] *= ORE_NUM_K[i]
	BLK_DATA[ore]['num'] = BLK_DATA[ore]['num'] * MAP_N * MAP_M // BLK_DENS_SIZE
	BLK_DATA[ore]['val'] *= ORE_VAL_K[i]
for i in range(0, CHEST_TOT):
	chest = CHESTS[i]
	BLK_DATA[chest]['num'] *= CHEST_NUM_K[i]
	BLK_DATA[chest]['num'] = BLK_DATA[chest]['num'] * MAP_N * MAP_M // BLK_DENS_SIZE
	BLK_DATA[chest]['val'] *= CHEST_VAL_K[i]

# NPC 移动概率
NPC_MOVE = [1, 100]

# 物块图片地址链接
DIRT_IMG_URL = './assets/img/dirt/{}.png'
ORE_IMG_URL = './assets/img/ore/{}.png'
CHEST_IMG_URL = './assets/img/chest/{}.png'
NPC_IMG_URL = './assets/img/npc/{}.png'
FOG_IMG_URL = './assets/img/fog.png'

# 背景相关常量
SKY, CLD, TREE, BIRD, UNDER, CAVE = 101, 102, 103, 104, 105, 106
P_SHOP, G_SHOP, O_SHOP, R_SHOP, D_SHOP = 111, 112, 113, 114, 115

# 图片列表长度
SKY_LEN, CLD_LEN, TREE_LEN, BIRD_LEN, UNDER_LEN, CAVE_LEN = 58, 35, 17, 13, 6, 6

# 云层、鸟的移动速度范围和方向
BG_DIR, BG_DIR_MP = [D_R, D_L], {D_R: D_D, D_L: D_U, D_D: D_R, D_U: D_L}
CLD_SPD = [1, 5]
BIRD_SPD = [1, 5]
# 云层、鸟的生成概率 [分子, 分母]
CLD_GEN_SPD = [1, 300]
BIRD_GEN_SPD = [1, 1000]
# 云层、鸟、树最大密度
BG_DENS_LEN = 1000
CLD_NUM_MAX, BIRD_NUM_MAX, TREE_NUM_MAX = 100, 100, 100

# 商店左侧第一列相较于出生点的偏移格数
SHOP_P = {
	P_SHOP: -12, G_SHOP: -7, O_SHOP: -2, R_SHOP: 4, D_SHOP: 9
}
SHOP_W = {
	P_SHOP: 4, G_SHOP: 4, O_SHOP: 5, R_SHOP: 4, D_SHOP: 4
}
SHOP_R = {
	P_SHOP: [SHOP_P[G_SHOP], SHOP_P[G_SHOP] + SHOP_W[G_SHOP] - 1],
	G_SHOP: [SHOP_P[P_SHOP], SHOP_P[P_SHOP] + SHOP_W[P_SHOP] - 1],
	O_SHOP: [SHOP_P[O_SHOP], SHOP_P[O_SHOP] + SHOP_W[O_SHOP] - 1],
	R_SHOP: [SHOP_P[R_SHOP], SHOP_P[R_SHOP] + SHOP_W[R_SHOP] - 1],
	D_SHOP: [SHOP_P[D_SHOP], SHOP_P[D_SHOP] + SHOP_W[D_SHOP] - 1],
}

# 油价, 气价, 维修价 （分子、分母）
P_COST, G_COST, R_COST = [1, 10], [1, 1], [1, 3]

SKY_IMG_URL = './assets/img/sky/{}.png'
CLD_IMG_URL = './assets/img/cloud/{}.png'
TREE_IMG_URL = './assets/img/tree/{}.png'
BIRD_IMG_URL = './assets/img/bird/{}.gif'
UNDER_IMG_URL = './assets/img/under/{}.png'
CAVE_IMG_URL = './assets/img/cave/{}.png'

SHOP_IMG_URL = {
	P_SHOP: './assets/img/shop/petrol.gif',
	G_SHOP: './assets/img/shop/gas.gif',
	O_SHOP: './assets/img/shop/ore.gif',
	R_SHOP: './assets/img/shop/repair.gif',
	D_SHOP: './assets/img/shop/drill.gif'
}
SHOP_COLORKEY = {
	P_SHOP: (225, 255, 210),
	G_SHOP: (45, 28, 24),
	O_SHOP: (92, 40, 43),
	R_SHOP: (0, 0, 0),
	D_SHOP: (142, 62, 156),
}

# 钻机物品 ID
BODY, HEAD, SFLAME, LFLAME = 201, 202, 203, 204

# 钻机参数常量
DRILL_LEVEL_MAX = 6
DRILL_DATA = {
	'rgd': [3, 6, 9, 12, 15, 18, 21],
	'h_max': [200, 400, 700, 1000, 1500, 3000, 5000],
	'g_max': [100, 150, 250, 400, 700, 1000, 1500],
	'p_max': [10000, 15000, 25000, 40000, 70000, 100000, 150000],
	'o_max': [50, 75, 110, 150, 200, 250, 300],
	'eng': [0, 1, 2, 3, 4, 5, 6],
}
DRILL_COST = {
	'rgd': [100, 200, 300, 400, 500, 600],
	'h_max': [102, 200, 300, 400, 500, 600],
	'g_max': [104, 200, 300, 400, 500, 600],
	'p_max': [103, 200, 300, 400, 500, 600],
	'o_max': [105, 200, 300, 400, 500, 600],
	'eng': [101, 200, 300, 400, 500, 600],
}
DRILL_LEVEL_COLOR = [
	(255, 221, 113),
	(193, 138, 234),
	(143, 255, 156),
	(117, 196, 255),
	(255, 139, 197),
	(255, 121, 121),
	(78, 248, 203)
]
HEAD_SHAKE = [-2, -2, -1, 1, 2, 2]
FLAME_SHAKE = [1, 1, 1, 0, -1, -1, -1, 0]

# 钻机速度 [分子, 分母] 像素每帧
SPEED_LEVEL = [
	[[0, -1], [1, 4], [1, 3], [1, 2], [1, 1], [2, 1], [3, 1], [4, 1], [6, 1], [12, 1]],
	[[0, -1], [1, 2], [2, 3], [1, 1], [2, 1], [4, 1], [6, 1], [8, 1], [12, 1], [24, 1]]
]
SPEED_LEVEL_MAX = len(SPEED_LEVEL[0]) - 1

# 钻机图片地址链接
DR_IMG_URL = {
	BODY: './assets/img/body/{}_{}.png',
	HEAD: './assets/img/head/{}_{}.png',
	SFLAME: './assets/img/sflame/{}_{}.png',
	LFLAME: './assets/img/lflame/{}_{}.png',
}

# 界面
P_ACHIEVE, P_INFO, P_KEYS, P_MENU, P_PAUSE = 301, 302, 303, 304, 305
P_READ, P_SAVE, P_YN, P_PSHOP, P_OVER = 306, 307, 308, 309, 310

PAGE_URL = {
	P_ACHIEVE: './assets/img/page/achieve.png',
	P_INFO: './assets/img/page/info.png',
	P_KEYS: './assets/img/page/keys.png',
	P_MENU: './assets/img/page/menu.png',
	P_PAUSE: './assets/img/page/pause.png',
	P_READ: './assets/img/page/read.png',
	P_SAVE: './assets/img/page/save.png',
	P_YN: './assets/img/page/YN.png',
	P_PSHOP: './assets/img/page/shop.png',
	P_OVER: './assets/img/page/over.png',
}

PAGE_NONE, PAGE_EXIT = 0, -1

LOG_NUM_MAX = 10
LOG_ROOT_URL = './.log'
LOG_INFO_EMPTY = '空存档'
LOG_INFO_FORM = '{}'
if not os.path.exists(LOG_ROOT_URL):
	os.mkdir(LOG_ROOT_URL)

PIXEL_FONT_URL = './assets/font/pixel-font.ttf'
LIGHT_GREEN = (127, 255, 127)
LIGHT_RED = (255, 127, 127)
DARK_RED = (255, 63, 63)
DARK_GREEN = (63, 176, 63)
P_COLOR = (255, 221, 113)
G_COLOR = (117, 196, 255)
O_COLOR = (200, 130, 4)
H_COLOR = DARK_RED

ACHIEVE_URL = './achieve'
ACHIEVE_DEFAULT = {}
for dirt in DIRTS:
	ACHIEVE_DEFAULT[dirt] = 0
ACHIEVE_DEFAULT['tot-dirt'] = 0
for ore in ORES:
	ACHIEVE_DEFAULT[ore] = 0
ACHIEVE_DEFAULT['tot-ore'] = 0
for chest in CHESTS:
	ACHIEVE_DEFAULT[chest] = 0
ACHIEVE_DEFAULT['tot-chest'] = 0
for npc in NPCS:
	ACHIEVE_DEFAULT[npc] = 0
ACHIEVE_DEFAULT['tot-npc'] = 0
ACHIEVE_DEFAULT['tot-money'] = 0
ACHIEVE_DEFAULT['tot-move'] = 0
if not os.path.exists(ACHIEVE_URL):
	open(ACHIEVE_URL, mode = 'w')

CG_IMG_URL = './assets/img/cg/{}.png'
CG_LEN = 7

default_font = pg.font.SysFont('kaiti', 20)
screen = pg.display.set_mode((SCR_W, SCR_H))
clock = pg.time.Clock()

image_buf = {}
for i in range(0, DIRT_TOT):
	tmp = DIRTS[i]
	image_buf[tmp] = pg.image.load(DIRT_IMG_URL.format(i))
for i in range(0, ORE_TOT):
	tmp = ORES[i]
	image_buf[tmp] = pg.image.load(ORE_IMG_URL.format(i))
for i in range(0, CHEST_TOT):
	tmp = CHESTS[i]
	image_buf[tmp] = pg.image.load(CHEST_IMG_URL.format(i))
for i in range(0, NPC_TOT):
	tmp = NPCS[i]
	image_buf[tmp] = pg.image.load(NPC_IMG_URL.format(i))
image_buf[FOG] = pg.image.load(FOG_IMG_URL)

press_sound = pg.mixer.Sound("./assets/audio/press.wav")
menu_sound = pg.mixer.Sound("./assets/audio/menu.wav")
menu_sound.set_volume(0.4)
land_sound = pg.mixer.Sound("./assets/audio/land.wav")
land_sound.set_volume(0.4)
under_sound = pg.mixer.Sound("./assets/audio/under.wav")
under_sound.set_volume(0.4)
dig_sound = pg.mixer.Sound("./assets/audio/dig.wav")
option_sound = pg.mixer.Sound("./assets/audio/option.wav")
drill_rgd_not_enough_sound = pg.mixer.Sound('./assets/audio/low_rgd.wav')
upgrade_sound = pg.mixer.Sound('./assets/audio/upgrade.wav')
dirt_break_sound = pg.mixer.Sound('./assets/audio/dirt_break.wav')
dirt_break_sound.set_volume(0.4)
unlock_chest_sound = pg.mixer.Sound('./assets/audio/unlock_chest.wav')
ore_break_sound = pg.mixer.Sound('./assets/audio/ore_break.wav')
fill_sound = pg.mixer.Sound('./assets/audio/fill.wav')
sell_sound = pg.mixer.Sound('./assets/audio/sell.wav')
save_npc_sound = [
	pg.mixer.Sound('./assets/audio/save_npc0.wav'),
	pg.mixer.Sound('./assets/audio/save_npc1.wav'),
	pg.mixer.Sound('./assets/audio/save_npc2.wav'),
	pg.mixer.Sound('./assets/audio/save_npc3.wav'),
	pg.mixer.Sound('./assets/audio/save_npc4.wav'),
	pg.mixer.Sound('./assets/audio/save_npc5.wav'),
]
audio_map = {
	"press_sound": press_sound,
	"menu_sound": menu_sound,
	"land_sound": land_sound,
	"under_sound": under_sound,
	"dig_sound": dig_sound,
	"option_sound": option_sound,
	'drill_rgd_not_enough_sound': drill_rgd_not_enough_sound
}


def swap(a, b):
	tmp = a
	a = b
	b = tmp


def b_to_p(r, c):
	x = (c - 1) * BLOCK_SZ
	y = (r - 1) * BLOCK_SZ
	return x, y


def scr_to_pos(r, c, rr, cc):
	r -= rr
	c += SCR_CEN_C - cc
	return r, c


def map_to_pos(r, c, rr, cc):
	return scr_to_pos(r + SCR_CEN_R, c, rr, cc)


def scr_b_to_p(r, c, rr, cc):
	r, c = scr_to_pos(r, c, rr, cc)
	x, y = b_to_p(r, c)
	return x, y


def map_b_to_p(r, c, rr, cc):
	r, c = map_to_pos(r, c, rr, cc)
	x, y = b_to_p(r, c)
	return x, y


def dr_b_to_p(r, c, dr_r, dr_c, mp_r, mp_c):
	r -= mp_r - dr_r
	c -= mp_c - dr_c
	x, y = b_to_p(r, c)
	return x, y


def get_rgd(tp):
	return BLK_DATA[tp]['rgd']


def get_damage(tp):
	return BLK_DATA[tp]['rgd']


def get_val(tp):
	return BLK_DATA[tp]['val']


def get_name(tp):
	return BLK_DATA[tp]['name']


def force_quit():
	pg.quit()
	exit(0)


def load_img(name: str):
	return pg.image.load(f'{name}')


def load_gif(name: str):
	images = []
	frames = imageio.mimread(name)
	for frame in frames:
		image = Image.fromarray(frame)
		images.append(pg.image.fromstring(image.tobytes(), image.size, image.mode))
	return images


def is_dirt(blk_tp):
	return DIRTS[0] <= blk_tp <= DIRTS[-1]


def is_ore(blk_tp):
	return ORES[0] <= blk_tp <= ORES[-1]


def is_chest(blk_tp):
	return CHESTS[0] <= blk_tp <= CHESTS[-1]


def is_NPC(blk_tp):
	return NPCS[0] <= blk_tp <= NPCS[-1]


def fog_dist(r, c, rr, cc):
	return abs(r - rr) + abs(c - cc)


def get_speed_level(blk_tp, dr_rgd_l, dr_eng_l, speedup):
	return SPEED_LEVEL[speedup][SPEED_LEVEL_MAX]
	dr_rgd = DRILL_DATA['rgd'][dr_rgd_l]
	dr_eng = DRILL_DATA['eng'][dr_eng_l]
	tmp = 4
	if is_dirt(blk_tp) or is_ore(blk_tp) or is_chest(blk_tp):
		blk_rgd = BLK_DATA[blk_tp]['rgd']
		tmp = min(dr_rgd - blk_rgd, tmp)
	if tmp < 0:
		drill_rgd_not_enough_sound.play()
		return SPEED_LEVEL[speedup][0]
	tmp += dr_eng + 1
	tmp = min(tmp, SPEED_LEVEL_MAX)
	return SPEED_LEVEL[speedup][tmp]


cur_bgm = "menu_sound"
audio_map[cur_bgm].play(-1)


def play_bgm(bgm):
	global cur_bgm
	if cur_bgm == bgm:
		pass
	else:
		audio_map[cur_bgm].stop()
		cur_bgm = bgm
		audio_map[cur_bgm].play(-1)


def pause_all_sound():
	pg.mixer.pause()


def resume_all_sound():
	pg.mixer.unpause()
