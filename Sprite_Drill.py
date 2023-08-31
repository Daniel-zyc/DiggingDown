from Constant import *
from Sprite import Sprite
import Global as glb


class Sprite_Drill(Sprite):
	def __init__(self, id, x, y):
		super().__init__()
		self.images = glb.load_images(f'{IMG_URL[id]}')
		self.image_indx = 0
		self.image = self.images[0]
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.image_roll = IMG_ROLL[id]
		self.image_roll_time = IMG_ROLL[id]

	def update(self):
		self.image_roll -= 1
		if self.image_roll == 0:
			self.image_roll = self.image_roll_time
			self.to_nxt_image()



