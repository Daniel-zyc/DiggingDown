from Constant import *


class SpriteGroup(pg.sprite.Group):
	def __init__(self):
		super().__init__()

	def move(self, d, sp):
		for obj in self.sprites():
			obj.move(d, sp)
