from Constant import *


class SpriteGroup(PG.sprite.Group):
	def __init__(self):
		super().__init__()

	def move(self, d, sp):
		for sprite in self.sprites():
			sprite.move(d, sp)
