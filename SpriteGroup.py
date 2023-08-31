from Constant import *


class SpriteGroup(pg.sprite.Group):
	def __init__(self):
		super().__init__()

	def move(self, d, sp):
		for sp in self.sprites():
			sp.move(d, sp)
