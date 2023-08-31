from Constant import *
from Sprite import Sprite
import ToolFunc as tool


class SpriteEasy(Sprite):
	def __init__(self, img_url: str, x = None, y = None):
		super().__init__()
		self.image = tool.load_sing_img(img_url)
		self.rect = self.image.get_rect()
		if y is not None:
			self.rect.x, self.rect.y = x, y
		else:
			self.rect.center = (SCR_CEN_X, SCR_CEN_Y)
