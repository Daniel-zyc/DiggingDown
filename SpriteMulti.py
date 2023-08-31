from Constant import *
from Sprite import Sprite


class SpriteMulti(Sprite):
	def __init__(self):
		super().__init__()
		self.images = self.image = None
		self.image_idx = self.image_timer = 0

	def roll_image(self):
		self.image_timer -= 1
		if self.image_timer < 0:
			self.image_idx += 1
			if self.image_idx >= len(self.images):
				self.image_idx = 0
			self.image = self.images[self.image_idx]
			self.image_timer = IMG_ROLL_SP // len(self.images)

