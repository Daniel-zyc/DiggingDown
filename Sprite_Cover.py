from Constant import *


class Sprite_Cover(PG.sprite.Sprite):
	def __init__(self, id, x, y):
		super().__init__()
		self.image = PG.image.load(f'{IMG_URL[id]}')
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y

	def move(self, d, sp):
		self.rect.x += D_XY[d][0] * sp
		self.rect.y += D_XY[d][1] * sp
