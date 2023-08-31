from Constant import *


class Control:
	def __init__(self):
		self.ctrls = {}
		for c in CTRL_LIST:
			self.ctrls[c] = 0

	def add_key(self, k: int, t: int):
		k = KEY_TO_CTRL[k]
		self.ctrls[k] = t

	def del_key(self, k: int):
		k = KEY_TO_CTRL[k]
		self.ctrls[k] = 0

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
