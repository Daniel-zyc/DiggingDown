import logging


class Page:
	def __init__(self):
		self.list = []
		self.update_range = None

	def draw(self, screen):
		for obj in self.list:
			obj.draw(screen)

	def __del__(self):
		for obj in self.list:
			obj.empty()
