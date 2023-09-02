import logging

from Constant import *
import functools


def swap(a, b):
	tmp = a
	a = b
	b = a


def b_to_p_tl(r, c):
	x = (c - 1) * BLOCK_SZ
	y = (r - 1) * BLOCK_SZ
	return x, y


def p_to_b_tl(x, y):
	r = y // BLOCK_SZ + 1
	c = x // BLOCK_SZ + 1
	return r, c


def loc_to_pos(r, c, rr, cc):
	r += (SCR_CEN_R - rr)
	c += (SCR_CEN_C - cc)
	return r, c


def loc_b_to_p(r, c, rr, cc):
	r, c = loc_to_pos(r, c, rr, cc)
	x, y = b_to_p_tl(r, c)
	return x, y


def force_quit():
	pg.quit()
	sys.exit(0)


@functools.lru_cache()
def load_sing_img(name: str):
	return pg.image.load(f'{name}')


def load_multi_img(name: str, arg1 = None, arg2 = None):
	logging.debug(f'load image: {name, arg1, arg2}')
	images = []
	i = 0
	filename = ''
	while True:
		if arg1 is None:
			filename = name.format(i)
		elif arg2 is None:
			filename = name.format(arg1, i)
		else:
			filename = name.format(arg1, arg2, i)
		if os.path.exists(filename):
			images.append(pg.image.load(filename))
		else:
			break
		i += 1
	logging.debug(f'total load: {len(images)}')
	return images


def get_speed_level(blk_tp, dr_rgd_l, dr_eng_l, speedup):
	dr_rgd = DRILL_DATA['rgd'][dr_rgd_l]
	dr_eng = DRILL_DATA['eng'][dr_eng_l]
	tmp = 4
	if blk_tp != EMPTY:
		blk_rgd = BLK_DATA[blk_tp]['rgd']
		tmp = min(dr_rgd - blk_rgd, tmp)
	if tmp < 0:
		return SPEED_LEVEL[speedup][0]
	tmp += dr_eng + 1
	tmp = min(tmp, SPEED_LEVEL_TOT - 1)
	return SPEED_LEVEL[speedup][tmp]
