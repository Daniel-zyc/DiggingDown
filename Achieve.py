from Constant import *
import atexit


class Achieve:
	def __init__(self):
		self.vals = ACHIEVE_DEFAULT
		with open(ACHIEVE_URL, mode = 'r') as f:
			s = f.readline()
			if s:
				self.vals = eval(s)

		atexit.register(self.__write)

	def __write(self):
		with open(ACHIEVE_URL, mode = 'w') as f:
			f.write(str(self.vals))



