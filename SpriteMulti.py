from Constant import *
from Sprite import Sprite
import ToolFunc as tool


class SpriteMulti(Sprite):
	def __init__(self, img_url = None, x = None, y = None, idx1 = None, idx2 = None):
		super().__init__()
		self.images = self.image = None
		self.image_idx = self.image_timer = 0
		if img_url is not None:
			self.images = tool.load_multi_img(img_url, idx1, idx2)
			self.image = self.images[self.image_idx]
			self.rect = self.image.get_rect()
			self.rect.x, self.rect.y = x, y

	def roll_image(self):
		self.image_timer -= 1
		if self.image_timer < 0:
			self.image_idx += 1
			if self.image_idx >= len(self.images):
				self.image_idx = 0
			self.image = self.images[self.image_idx]
			self.image_timer = IMG_ROLL_SP // len(self.images)

	def flip_images(self, arg1 = True, arg2 = False):
		for i in range(0, len(self.images)):
			self.images[i] = pg.transform.flip(self.images[i], arg1, arg2)

	def set_colorkey(self, color):
		for img in self.images:
			img.set_colorkey(color)

	def update(self):
		self.roll_image()
