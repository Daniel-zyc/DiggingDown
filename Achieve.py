from Constant import *
import atexit


class Achieve:
	def __init__(self):
		self.vals = [0 for i in range(0, ACHIEVE_TOT)]
		with open(ACHIEVE_URL, mode = 'r') as f:
			s = f.readline()
			if s:
				self.vals = eval(s)
		atexit.register(self.__write)

	def __write(self):
		with open(ACHIEVE_URL, mode = 'w') as f:
			f.write(str(self.vals))



