from Constant import *
from Sprite import Sprite
import Global as glb


class Sprite_Block(Sprite):
	def __init__(self, id, x, y):
		super().__init__()
		self.image = glb.load_image(f'{IMG_URL[id]}')
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
