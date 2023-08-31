from Constant import *


class Key:
	def __init__(self, val: int, time: int):
		if val in KEY_TO_CTRL:
			self.val = KEY_TO_CTRL[val]
		else:
			self.val = CTRL_NONE
		self.time = time


class Control:
	def __init__(self):
		self.ctrls = {}
		for ctrl in CTRL_LIST:
			self.ctrls[ctrl] = 0

	def add_key(self, key: Key):
		self.ctrls[key.val] = key.time

	def del_key(self, key: Key):
		self.ctrls[key.val] = 0

	def get_short_key(self, *args):
		ret, time = CTRL_NONE, 0
		for arg in args:
			if self.ctrls[arg] > self.ctrls[ret]:
				ret, time = arg, self.ctrls[arg]
		self.ctrls[ret] = 0
		if ret != CTRL_NONE:
			logging.debug(f'Control.get_short_key: {ret}')
		return ret

	def get_long_key(self, *args):
		ret, time = CTRL_NONE, 0
		for arg in args:
			if self.ctrls[arg] > self.ctrls[ret]:
				ret, time = arg, self.ctrls[arg]
		if ret != CTRL_NONE:
			logging.debug(f'Control.get_long_key: {ret}')
		return ret

	def chk_key(self, *args):
		ret, time = CTRL_NONE, 0
		for arg in args:
			if self.ctrls[arg] > self.ctrls[ret]:
				ret, time = arg, self.ctrls[arg]
		return ret != CTRL_NONE
