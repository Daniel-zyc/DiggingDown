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


def force_quit():
	pg.quit()
	sys.exit(0)


@functools.lru_cache()
def load_sing_img(name: str):
	return pg.image.load(f'{name}')


@ functools.lru_cache()
def load_multi_img(name: str, arg = None):
	images = []
	i = 0
	filename = ''
	while True:
		if arg is None:
			filename = name.format(i)
		else:
			filename = name.format(arg, i)
		if os.path.exists(filename):
			images.append(pg.image.load(filename))
		else:
			break
		i += 1
	return images
