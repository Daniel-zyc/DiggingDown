from Constant import *
from Sprite import Sprite


class SpriteMulti(Sprite):
	def __init__(self, img_url, x = None, y = None):
		super().__init__()
		self.image_idx = self.image_timer = 0
		self.images = load_gif(img_url)
		self.image = self.images[self.image_idx]
		self.rect = self.image.get_rect()
		if y is not None:
			self.rect.x, self.rect.y = x, y
		else:
			self.rect.center = (SCR_CEN_X, SCR_CEN_Y)

	def roll_image(self):
		self.image_timer -= 1
		if self.image_timer < 0:
			self.image_idx += 1
			if self.image_idx >= len(self.images):
				self.image_idx = 0
			self.image = self.images[self.image_idx]
			self.image_timer = IMG_ROLL_SPD // len(self.images)

	def flip_images(self, arg1 = True, arg2 = False):
		for i in range(0, len(self.images)):
			self.images[i] = pg.transform.flip(self.images[i], arg1, arg2)

	def set_colorkey(self, color):
		for img in self.images:
			img.set_colorkey(color)

	def update(self):
		self.roll_image()
