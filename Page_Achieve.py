from Constant import *
from PageEasy import PageEasy
from SpriteEasy import SpriteEasy
import Global as glb


class Page_Achieve(PageEasy):
	def __init__(self):
		super().__init__(SpriteEasy(PAGE_URL[P_ACHIEVE]))
		self.data = glb.achieve.vals
