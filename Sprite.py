from Constant import *


class Sprite(PG.sprite.Sprite):
	def __init__(self):
		super().__init__()
		self.images = self.image = self.image_indx = self.rect = None

	def move(self, d, sp):
		self.rect.x += D_XY[d][0]*sp
		self.rect.y += D_XY[d][1]*sp

	def to_nxt_image(self):
		self.image_indx += 1
		self.image_indx %= len(self.images)
		self.image = self.images[self.image_indx]
