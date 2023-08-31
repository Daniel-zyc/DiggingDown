class Page:
	def __init__(self):
		self.spg_list = []
		self.update_range = None

	def draw(self, scr):
		for spg in self.spg_list:
			spg.draw(scr)

	def __del__(self):
		for spg in self.spg_list:
			spg.empty()
