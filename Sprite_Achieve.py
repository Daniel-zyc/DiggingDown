from Constant import *


class Sprite_Achieve(PG.sprite.Sprite):
	def __init__(self):
		super().__init__()
		self.image = PG.image.load(f'./assets/img/achieve/page.png')
		self.rect = self.image.get_rect()
		self.rect.center = (SCR_CEN_X, SCR_CEN_Y)
