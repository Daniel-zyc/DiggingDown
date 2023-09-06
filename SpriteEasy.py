from Constant import *
from Sprite import Sprite


class SpriteEasy(Sprite):
	def __init__(self, img_url: str, x = None, y = None, k = None):
		super().__init__()
		self.image = load_img(img_url)
		if k is not None:
			self.image = pg.transform.scale(self.image, (k * self.image.get_width(), k * self.image.get_height()))
		self.rect = self.image.get_rect()
		if y is not None:
			self.rect.x, self.rect.y = x, y
		else:
			self.rect.center = (SCR_CEN_X, SCR_CEN_Y)
