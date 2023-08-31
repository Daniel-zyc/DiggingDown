from Constant import *


class Sprite(pg.sprite.Sprite):
	def __init__(self):
		super().__init__()
		self.rect = None

	def move(self, d: int, sp: int):
		self.rect.x += D_XY[d][0] * sp
		self.rect.y += D_XY[d][1] * sp
