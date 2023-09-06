from Constant import *


class Control:
	def __init__(self):
		self.ctrls = {}
		for c in CTRL_LIST:
			self.ctrls[c] = 0
		self.mouse_pos = None

	def add_key(self, k: int, key_time: int):
		if k in KEY_TO_CTRL:
			k = KEY_TO_CTRL[k]
			self.ctrls[k] = key_time

	def del_key(self, k: int):
		if k in KEY_TO_CTRL:
			k = KEY_TO_CTRL[k]
			self.ctrls[k] = 0

	def mouse_down(self, pos):
		self.mouse_pos = pos

	def mouse_up(self):
		self.mouse_pos = None

	def get_click(self, rect: pg.Rect):
		if self.mouse_pos is None:
			return 0
		if rect.collidepoint(self.mouse_pos):
			self.mouse_pos = None
			return True
		return False

	def get_key(self, *args: int):
		c, t = CTRL_NONE, 0
		for arg in args:
			if self.ctrls[arg] > self.ctrls[c]:
				c, t = arg, self.ctrls[arg]
		self.ctrls[c] = 0
		if c != CTRL_NONE: logging.debug(f'controller get key: {c}')
		return c

	def get_press(self, *args: int):
		c, t = CTRL_NONE, 0
		for arg in args:
			if self.ctrls[arg] > self.ctrls[c]:
				c, t = arg, self.ctrls[arg]
		if c != CTRL_NONE: logging.debug(f'controller get press: {c}')
		return c

	def clear(self):
		self.ctrls = {}
		for c in CTRL_LIST:
			self.ctrls[c] = 0
		self.mouse_pos = None
