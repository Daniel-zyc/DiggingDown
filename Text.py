from Constant import *


class Text:
	def __init__(self):
		self.list = []

	def add(self, s, x = 0, y = 0, font = default_font, color = (0, 0, 0)):
		text = font.render(s, True, color)
		rect = text.get_rect()
		rect.x = x
		rect.y = y
		self.list.append([text, rect])
		return rect

	def add_row(self, s, x = 0, gap = FONT_SIZE + 4, font = default_font, color = (0, 0, 0)):
		text = font.render(s, True, color)
		rect = text.get_rect()
		rect.x = x
		if len(self.list) == 0:
			rect.y = 0
		else:
			rect.y = self.list[-1][1].y + gap
		self.list.append([text, rect])
		return rect

	def clear(self):
		self.list.clear()

	def draw(self, screen):
		for t, r in self.list:
			screen.blit(t, r)
