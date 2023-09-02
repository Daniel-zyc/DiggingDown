from Constant import *
from SpriteMulti import SpriteMulti
import ToolFunc as tool


class Sprite_Cloud(SpriteMulti):
	def __init__(self, idx, d, sp, x, y):
		super().__init__()
		self.images = tool.load_multi_img(BG_IMG_URL[CLOUD], idx)
		self.image = self.images[self.image_idx]
		self.rect = self.image.get_rect()
		if d == 0:
			self.rect.topright = (x, y)
		else:
			self.rect.x, self.rect.y = x, y
		self.d, self.sp = d, sp
		if self.d == D_L:
			for img in self.images:
				pg.transform.flip(img, True, False)

	def update(self):
		self.move(CLOUD_DIR[self.d], self.sp)
		self.roll_image()

	def check_in_map(self, left, width):
		if self.d == 0:
			return self.rect.x <= left + width
		else:
			return self.rect.right >= left
