import functools

from Constant import *
from Control import Control, Key
from Page_Y_or_N import Page_Y_or_N

screen = PG.display.set_mode((SCR_W, SCR_H))
clock = PG.time.Clock()
ctrl = Control()
frame_time = key_time = 0
pages = []


def swap(a, b):
	return b, a


def b_to_p_tl(r, c):
	x = (c-1) * BLOCK_SZ
	y = (r-1) * BLOCK_SZ
	return x, y


def p_to_b_tl(x, y):
	r = y // BLOCK_SZ + 1
	c = x // BLOCK_SZ + 1
	return r, c


def window_refresh_display():
	PG.draw.rect(screen, (0, 0, 0), pages[-1].update_range)
	pages[-1].draw(screen)
	PG.display.update(pages[-1].update_range)


def get_Y_or_N():
	global frame_time, key_time
	pages.append(Page_Y_or_N())
	window_refresh_display()
	ret = False
	while True:
		clock.tick(FPS)
		frame_time += 1

		for event in PG.event.get():
			if event.type == PG.KEYDOWN:
				key_time += 1
				ctrl.add_key(Key(event.key, key_time))
			elif event.type == PG.KEYUP:
				key_time += 1
				ctrl.del_key(Key(event.key, key_time))

		status, data = pages[-1].refresh(ctrl)
		if status == PAGE_NONE:
			continue
		if status == PAGE_EXIT:
			ret = data
			break
	pages.pop()
	return ret


def get_speed_level(blk_tp, dr_tp, speedup):
	blk_rgd = 0
	if blk_tp in ORES_DATA:
		blk_rgd = ORES_DATA[blk_tp]['rgd']
	elif blk_tp == DIRT:
		blk_rgd = 1
	dr_rgd = DRILL_DATA[dr_tp]['rgd']
	if dr_rgd < blk_rgd:
		return SPEED_LEVEL[speedup][0]
	else:
		return SPEED_LEVEL[speedup][dr_rgd - blk_rgd + 1]


@functools.lru_cache()
def load_image(name: str):
	return PG.image.load(f'{name}')


@functools.lru_cache()
def load_images(name: str):
	images = []
	i = 0
	while True:
		filename = name.format(i)
		# logging.debug(f'load_filename: {filename}')
		if os.path.exists(filename):
			images.append(PG.image.load(filename))
		else:
			break
		i += 1
	# logging.debug(f'load_images: {len(images)}')
	return images



